from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data_closest_date
from hestia_earth.utils.tools import non_empty_list, safe_parse_float, flatten

from hestia_earth.aggregation.log import logger
from hestia_earth.aggregation.utils import _aggregated_version
from hestia_earth.aggregation.utils.impact_assessment import (
    _create_impact_assessment, _impact_assessment_id,
    _impact_assessment_name, _group_impacts_by_product, _impact_assessment_year
)
from hestia_earth.aggregation.utils.indicator import _new_indicator

AGGREGATION_KEY = 'emissionsResourceUse'


def _organic_weight(country_id: str, year: int):
    lookup = download_lookup('region-standardsLabels-isOrganic.csv', True)
    data = get_table_value(lookup, 'termid', country_id, 'organic')
    percent = extract_grouped_data_closest_date(data, year)
    percent = safe_parse_float(percent, 100) / 100
    logger.debug('organic weight, country=%s, year=%s, percent=%s', country_id, year, percent)
    return percent


def _irrigated_weight(country_id: str, year: int):
    lookup = download_lookup('region-irrigated.csv', True)
    irrigated_data = get_table_value(lookup, 'termid', country_id, column_name('irrigatedValue'))
    irrigated = extract_grouped_data_closest_date(irrigated_data, year)
    area_data = get_table_value(lookup, 'termid', country_id, column_name('totalCroplandArea'))
    area = extract_grouped_data_closest_date(area_data, year)
    percent = safe_parse_float(irrigated, 1) / safe_parse_float(area, 1)
    logger.debug('irrigated weight, country=%s, year=%s, percent=%s', country_id, year, percent)
    return percent


def _weighted_value(country_id: str, year: int):
    def apply(indicator: dict):
        organic_weight = _organic_weight(country_id, year)
        irrigated_weight = _irrigated_weight(country_id, year)
        weight = (
            organic_weight if indicator.get('organic', False) else 1-organic_weight
        ) * (
            irrigated_weight if indicator.get('irrigated', False) else 1-irrigated_weight
        )
        return indicator.get('value'), weight
    return apply


def _aggregate_weighted_indicators(country_id: str, year: int, term: dict, indicators: list, product: dict):
    values = list(map(_weighted_value(country_id, year), indicators))
    value = sum([value * weight for value, weight in values])
    percent = sum(weight for _v, weight in values)
    value = value / percent if percent != 0 else value
    indicator = _new_indicator(term)
    logger.debug('product=%s, country=%s, year=%s, term: %s, value: %s',
                 product.get('@id'), country_id, str(year), term.get('@id'), str(value))
    indicator['value'] = value
    indicator['observations'] = sum([indicator.get('observations', 1) for indicator in indicators])
    return _aggregated_version(indicator, 'value', 'observations')


def _aggregate_country_impact(data: dict):
    product = data.get('product')
    impacts = data.get('impacts', [])
    impact = impacts[0]
    country_id = impact.get('country').get('@id')
    year = _impact_assessment_year(impact)

    def aggregate(term_id: str):
        indicators = data.get('indicators').get(term_id)
        term = indicators[0].get('term')
        return _aggregate_weighted_indicators(country_id, year, term, indicators, product)

    aggregates = flatten(map(aggregate, data.get('indicators', {}).keys()))
    impact = _create_impact_assessment(impact)
    impact['organic'] = False
    impact['irrigated'] = False
    impact[AGGREGATION_KEY] = aggregates
    impact['name'] = _impact_assessment_name(impact, False)
    impact['id'] = _impact_assessment_id(impact, False)
    return impact if len(aggregates) > 0 else None


def aggregate(impacts: list) -> list:
    grouped_impacts = _group_impacts_by_product(impacts, False)
    result = non_empty_list([
        _aggregate_country_impact(value) for value in grouped_impacts.values()
    ])
    return impacts + result
