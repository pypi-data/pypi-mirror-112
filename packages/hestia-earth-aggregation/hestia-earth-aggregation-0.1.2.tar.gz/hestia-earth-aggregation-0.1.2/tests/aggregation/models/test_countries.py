import json

from tests.utils import fixtures_path, start_year, end_year
from hestia_earth.aggregation.models.countries import aggregate, _aggregate_weighted_indicators
from hestia_earth.aggregation.utils.impact_assessment import _update_impact_assessment

class_path = 'hestia_earth.aggregation.models.countries'


def test_aggregate():
    with open(f"{fixtures_path}/impact-assessment/terms/aggregated.jsonld", encoding='utf-8') as f:
        impacts = json.load(f)
    with open(f"{fixtures_path}/impact-assessment/countries/aggregated.jsonld", encoding='utf-8') as f:
        expected = json.load(f)
    results = aggregate(impacts)
    results = list(map(
        lambda result: _update_impact_assessment(result['country'], start_year, end_year)(result), results))
    assert results == expected
    assert len(results) == 11 + 6  # 11 from terms and 6 new


def test_aggregate_weighted_indicators():
    country_id = 'GADM-AUS'
    year = 2000
    term = {'@id': 'term'}
    product = {'@id': 'product'}
    indicators = [{
        'organic': True,
        'irrigated': True,
        'value': 5
    }, {
        'organic': True,
        'irrigated': False,
        'value': 10
    }, {
        'organic': False,
        'irrigated': False,
        'value': 1
    }]
    indicator = _aggregate_weighted_indicators(country_id, year, term, indicators, product)
    assert indicator.get('value') == 1.0940374220686617
