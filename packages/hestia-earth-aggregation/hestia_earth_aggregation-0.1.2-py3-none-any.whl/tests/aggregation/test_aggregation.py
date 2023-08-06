from unittest.mock import patch
import pytest

from tests.utils import start_year, end_year
from hestia_earth.aggregation import aggregate, _aggregate_by_country, _aggregate_global

class_path = 'hestia_earth.aggregation.aggregation'


@patch('hestia_earth.aggregation.get_time_ranges', return_value=[[2001, 2010]])
@patch('hestia_earth.aggregation._aggregate_by_country', return_value=[])
@patch('hestia_earth.aggregation._aggregate_global', return_value=[])
def test_aggregate(mock_aggregate_global, mock_aggregate_by_country, *args):
    # without a country
    aggregate()
    mock_aggregate_global.assert_called_once()
    mock_aggregate_by_country.assert_not_called()

    mock_aggregate_global.reset_mock()
    mock_aggregate_by_country.reset_mock()

    # with country None
    aggregate(country_name=None)
    mock_aggregate_global.assert_called_once()
    mock_aggregate_by_country.assert_not_called()

    mock_aggregate_global.reset_mock()
    mock_aggregate_by_country.reset_mock()

    # without country
    aggregate(country_name='Japan')
    mock_aggregate_global.assert_not_called()
    mock_aggregate_by_country.assert_called_once()


@patch('hestia_earth.aggregation._global_impacts_by_product', return_value={})
@patch('hestia_earth.aggregation.aggregate_world')
def test_aggregate_global(mock_aggregate, *args):
    _aggregate_global(start_year, end_year)
    mock_aggregate.assert_called_once()


@patch('hestia_earth.aggregation._fetch_single', return_value=None)
def test_aggregate_by_country_not_found(*args):
    country_name = 'Japan'
    with pytest.raises(Exception):
        _aggregate_by_country(start_year, end_year, country_name)


@patch('hestia_earth.aggregation._fetch_single', return_value={})
@patch('hestia_earth.aggregation._all_impacts_by_product', return_value={})
@patch('hestia_earth.aggregation.aggregate_by_country', return_value=[])
@patch('hestia_earth.aggregation.aggregate_by_term')
def test_aggregate_by_country(mock_aggregate, *args):
    country_name = 'Japan'
    _aggregate_by_country(start_year, end_year, country_name=country_name)
    mock_aggregate.assert_called_once()
