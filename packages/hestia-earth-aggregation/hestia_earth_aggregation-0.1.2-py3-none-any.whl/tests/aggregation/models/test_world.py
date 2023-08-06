import json

from tests.utils import fixtures_path, start_year, end_year
from hestia_earth.aggregation.models.world import aggregate
from hestia_earth.aggregation.utils.impact_assessment import _group_impacts_by_product, _update_impact_assessment

class_path = 'hestia_earth.aggregation.models.world'


def test_aggregate():
    with open(f"{fixtures_path}/impact-assessment/countries/aggregated.jsonld", encoding='utf-8') as f:
        impacts = json.load(f)
    with open(f"{fixtures_path}/impact-assessment/world/aggregated.jsonld", encoding='utf-8') as f:
        expected = json.load(f)
    impacts_by_product = _group_impacts_by_product(impacts, False)
    results = aggregate(impacts_by_product)
    results = list(map(_update_impact_assessment({'@id': 'region-world'}, start_year, end_year), results))
    assert results == expected
    assert len(results) == 6
