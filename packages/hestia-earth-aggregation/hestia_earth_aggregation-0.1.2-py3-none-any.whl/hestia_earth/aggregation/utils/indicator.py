from hestia_earth.schema import IndicatorJSONLD, IndicatorStatsDefinition
from hestia_earth.utils.model import linked_node

from . import _aggregated_version


def _new_indicator(term: dict):
    indicator = IndicatorJSONLD().to_dict()
    indicator['term'] = linked_node(term)
    indicator['statsDefinition'] = IndicatorStatsDefinition.IMPACTASSESSMENTS.value
    return _aggregated_version(indicator, 'term', 'statsDefinition')
