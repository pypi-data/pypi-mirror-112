from hestia_earth.schema import TermTermType
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data_closest_date
from hestia_earth.utils.tools import non_empty_list, safe_parse_float, flatten

from hestia_earth.aggregation.log import logger
from hestia_earth.aggregation.utils import _aggregated_version
from hestia_earth.aggregation.utils.term import DEFAULT_REGION_ID
from hestia_earth.aggregation.utils.impact_assessment import _create_impact_assessment
from hestia_earth.aggregation.utils.indicator import _new_indicator

AGGREGATION_KEY = 'emissionsResourceUse'
LOOKUP_GROUPING = {
    TermTermType.CROP.value: download_lookup(f"{TermTermType.CROP.value}.csv", True),
    TermTermType.ANIMALPRODUCT.value: download_lookup(f"{TermTermType.ANIMALPRODUCT.value}.csv", True)
}
LOOKUP_GROUPING_COLUMN = {
    TermTermType.CROP.value: 'cropGroupingFAOSTAT',
    TermTermType.ANIMALPRODUCT.value: 'animalProductGroupingFAO'
}


def _lookup(product: dict):
    term_type = product.get('termType')
    try:
        lookup = LOOKUP_GROUPING[term_type]
        grouping_column = LOOKUP_GROUPING_COLUMN[term_type]
        grouping = get_table_value(lookup, 'termid', product.get('@id'), column_name(grouping_column))
        return download_lookup(f"region-{term_type}-{grouping_column}-productionQuantity.csv", True), grouping
    except Exception:
        return None, None


def _get_weight(lookup, lookup_column: str, country_id: str, year: int):
    country_value = get_table_value(lookup, 'termid', country_id, column_name(lookup_column))
    country_value = extract_grouped_data_closest_date(country_value, year)
    world_value = get_table_value(lookup, 'termid', DEFAULT_REGION_ID, column_name(lookup_column))
    world_value = extract_grouped_data_closest_date(world_value, year)
    percent = safe_parse_float(country_value, 1) / safe_parse_float(world_value, 1)
    logger.debug('weight, country=%s, year=%s, percent=%s', country_id, year, percent)
    return percent


def _weighted_value(lookup, lookup_column: str):
    def apply(indicator: dict):
        country_id = indicator.get('country').get('@id')
        weight = _get_weight(lookup, lookup_column, country_id, indicator.get('year')) if lookup is not None else 1
        return indicator.get('value'), weight
    return apply


def _aggregate_indicators(term: dict, indicators: list, product: dict):
    lookup, lookup_column = _lookup(product)
    values = list(map(_weighted_value(lookup, lookup_column), indicators))
    value = sum([value * weight for value, weight in values])
    percent = sum(weight for _v, weight in values)
    value = value / percent if percent != 0 else value
    indicator = _new_indicator(term)
    logger.debug('product=%s, term: %s, value: %s', product.get('@id'), term.get('@id'), str(value))
    indicator['value'] = value
    indicator['observations'] = sum([indicator.get('observations', 1) for indicator in indicators])
    return _aggregated_version(indicator, 'value', 'observations')


def _aggregate_world_impact(data: dict):
    product = data.get('product')
    impacts = data.get('impacts', [])

    def aggregate(term_id: str):
        indicators = data.get('indicators').get(term_id)
        term = indicators[0].get('term')
        return _aggregate_indicators(term, indicators, product)

    aggregates = flatten(map(aggregate, data.get('indicators', {}).keys()))
    impact = _create_impact_assessment(impacts[0])
    impact['organic'] = False
    impact['irrigated'] = False
    impact[AGGREGATION_KEY] = aggregates
    return impact if len(aggregates) > 0 else None


def aggregate(impacts_per_product: dict) -> list:
    return non_empty_list([
        _aggregate_world_impact(value) for value in impacts_per_product.values()
    ])
