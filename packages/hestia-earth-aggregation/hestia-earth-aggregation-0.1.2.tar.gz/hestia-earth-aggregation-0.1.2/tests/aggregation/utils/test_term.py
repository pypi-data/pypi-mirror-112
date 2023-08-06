from unittest.mock import patch
from hestia_earth.schema import TermTermType

from hestia_earth.aggregation.utils.term import _fetch_all

class_path = 'hestia_earth.aggregation.utils.term'


@patch(f"{class_path}.find_node", return_value=[])
def test_fetch_all(mock_find_node):
    _fetch_all(TermTermType.EMISSION)
    mock_find_node.assert_called_once()
