from unittest.mock import patch, MagicMock

from tests.utils import IMPACTS, start_year, end_year
from hestia_earth.aggregation.utils.impact_assessment import (
    _download_impact, _download_impacts, _all_impacts,
    _group_impacts_by_product, _all_impacts_by_product, _global_impacts_by_product, _update_impact_assessment,
    get_time_ranges, _format_country_name
)

class_path = 'hestia_earth.aggregation.utils.impact_assessment'
country_name = 'Japan'


class FakePostRequest():
    def __init__(self, results=[]) -> None:
        self.results = results
        pass

    def json(self):
        return {'results': self.results}


@patch(f"{class_path}.download_hestia", return_value={})
def test_download_impact(mock_download_hestia):
    _download_impact('')({})
    mock_download_hestia.assert_called_once()


@patch(f"{class_path}._download_impact")
def test_download_impacts(mock_download):
    mock = MagicMock()
    mock_download.return_value = mock
    impacts = [{}, {}]
    _download_impacts(impacts)
    assert mock.call_count == len(impacts)


def test_group_impacts_by_product():
    results = _group_impacts_by_product(IMPACTS, True)
    assert len(results.keys()) == 11

    # non-including organic/irrigated matrix
    results = _group_impacts_by_product(IMPACTS, False)
    assert len(results.keys()) == 6


@patch('requests.post', return_value=FakePostRequest())
def test_all_impacts(mock_post):
    _all_impacts(start_year, end_year, 'Japan')
    mock_post.assert_called_once()


@patch(f"{class_path}._all_impacts", return_value=[])
@patch(f"{class_path}._download_impacts", return_value=[])
def test_all_impacts_by_product(mock_download, *args):
    _all_impacts_by_product(start_year, end_year, 'Japan')
    mock_download.assert_called_once_with([], data_state='recalculated')


@patch('requests.post', return_value=FakePostRequest())
@patch(f"{class_path}._download_impacts", return_value=[])
def test_global_impacts_by_product(mock_download, *args):
    _global_impacts_by_product(start_year, end_year)
    mock_download.assert_called_once_with([])


@patch(f"{class_path}._format_country_name", side_effect=lambda n: n)
@patch(f"{class_path}._fetch_single", side_effect=lambda v: {'name': v})
def test_update_impact_assessment(*args):
    impact = {}
    result = _update_impact_assessment(country_name, start_year, end_year)(impact)
    assert result == {
        'id': f"{country_name}-{start_year}-{end_year}-conventional-non-irrigated",
        'name': f"{country_name} - Conventional, Non Irrigated - {start_year}-{end_year}",
        'country': {
            '@type': 'Term',
            'name': country_name
        },
        'startDate': str(start_year),
        'endDate': str(end_year)
    }

    # with a source
    source = {'@type': 'Source', '@id': 'source'}
    result = _update_impact_assessment(country_name, start_year, end_year, source)(impact)
    assert result == {
        'id': f"{country_name}-{start_year}-{end_year}-conventional-non-irrigated",
        'name': f"{country_name} - Conventional, Non Irrigated - {start_year}-{end_year}",
        'country': {
            '@type': 'Term',
            'name': country_name
        },
        'startDate': str(start_year),
        'endDate': str(end_year),
        'source': source
    }


@patch('requests.post')
def test_get_time_ranges(mock_post):
    mock_post.return_value = FakePostRequest([{'endDate': '1996'}])
    assert get_time_ranges(country_name) == [[1990, 1999], [2000, 2009], [2010, 2019], [2020, 2029]]

    mock_post.return_value = FakePostRequest([{'endDate': '2000'}])
    assert get_time_ranges(country_name) == [[2000, 2009], [2010, 2019], [2020, 2029]]


def test_format_country_name():
    assert _format_country_name('Virgin Islands, U.S.') == 'virgin-islands-us'
    assert _format_country_name('Turkey (Country)') == 'turkey-country'
    assert _format_country_name("Côte d'Ivoire") == 'cote-divoire'
    assert _format_country_name('Åland') == 'aland'
    assert _format_country_name('Réunion') == 'reunion'
    assert _format_country_name('São Tomé and Príncipe') == 'sao-tome-and-principe'
