from functools import reduce
import requests
import json
import math
import re
from unidecode import unidecode
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.tools import non_empty_list, safe_parse_date
from hestia_earth.utils.request import api_url
from hestia_earth.utils.model import linked_node

from ..log import logger
from .term import DEFAULT_COUNTRY_NAME, _fetch_single
from .source import HESTIA_BIBLIO_TITLE

SEARCH_LIMIT = 10000
# exclude ImpactAssessment from ecoinvent
EXCLUDE_BIBLIOS = [
    HESTIA_BIBLIO_TITLE,
    'The ecoinvent database version 3 (part I): overview and methodology'
]


def _date_range_query(start: int, end: int): return {'range': {'endDate': {'gte': str(start), 'lte': str(end)}}}


def _source_query(title: str): return {'match': {'source.bibliography.title.keyword': title}}


def _impacts_query():
    return {
        'bool': {
            'must': [{'match': {'@type': SchemaType.IMPACTASSESSMENT.value}}],
            'must_not': list(map(_source_query, EXCLUDE_BIBLIOS))
        }
    }


def _country_query(country_name: str): return {'match': {'country.name.keyword': country_name}}


def _run_query(data: dict):
    headers = {'Content-Type': 'application/json'}
    params = json.dumps(data)
    logger.debug('Running query: %s', params)
    return requests.post(f'{api_url()}/search', params, headers=headers).json().get('results', [])


def _all_impacts(start_year: int, end_year: int, country_name: str):
    query = _impacts_query()
    query['bool']['must'].append(_date_range_query(start_year, end_year))
    if country_name != DEFAULT_COUNTRY_NAME:
        query['bool']['must'].append(_country_query(country_name))

    return _run_query({
        'query': query,
        'limit': SEARCH_LIMIT,
        'fields': ['@id']
    })


def _earliest_impact_date(country_name: str):
    query = _impacts_query()
    if country_name and country_name != DEFAULT_COUNTRY_NAME:
        query['bool']['must'].append(_country_query(country_name))
    params = {
        'query': query,
        'limit': 1,
        'fields': ['endDate'],
        'sort': [{'endDate.keyword': 'asc'}]
    }
    results = _run_query(params)
    return results[0].get('endDate') if len(results) > 0 else None


def _download_impact(data_state=''):
    def download(n):
        try:
            node = download_hestia(n.get('@id'), SchemaType.IMPACTASSESSMENT, data_state=data_state)
            return node if node.get('@type') else None
        except Exception:
            logger.debug('skip non-%s impact_assessment: %s', data_state, n.get('@id'))
            return None
    return download


def _download_impacts(impacts: list, data_state=''):
    total = len(impacts)
    with ThreadPoolExecutor() as executor:
        impacts = non_empty_list(executor.map(_download_impact(data_state), impacts))
    logger.debug('downloaded %s impacts / %s total impacts', str(len(impacts)), str(total))
    return impacts


def _all_impacts_by_product(start_year: int, end_year: int, country_name: str):
    # TODO: paginate search and improve performance
    impacts = _all_impacts(start_year, end_year, country_name)
    impacts = _download_impacts(impacts, data_state='recalculated')
    return _group_impacts_by_product(impacts)


def _global_impacts_by_product(start_year: int, end_year: int):
    impacts = _run_query({
        'query': {
            'bool': {
                'must': [
                    {'match': {'@type': SchemaType.IMPACTASSESSMENT.value}},
                    _source_query(HESTIA_BIBLIO_TITLE),
                    _date_range_query(start_year, end_year)
                ],
                'must_not': [
                    _country_query(DEFAULT_COUNTRY_NAME)
                ]
            }
        },
        'limit': SEARCH_LIMIT,
        'fields': ['@id']
    })
    impacts = _download_impacts(impacts)
    return _group_impacts_by_product(impacts, False)


def _group_indicators(group: dict, indicator: dict):
    term_id = indicator.get('term', {}).get('@id')
    if term_id not in group:
        group[term_id] = []
    group[term_id].append(indicator)
    return group


def _group_impacts_by_product(impacts: list, include_matrix=True) -> dict:
    def group_by(group: dict, impact: dict):
        organic = impact.get('organic', False)
        irrigated = impact.get('irrigated', False)
        key = '-'.join([
            str(organic),
            str(irrigated),
            impact.get('product').get('@id')
        ]) if include_matrix else impact.get('product').get('@id')
        if key not in group:
            group[key] = {
                'product': impact.get('product'),
                'impacts': [],
                'indicators': {}
            }
        group[key]['impacts'].append(impact)
        # save ref to organic/irrigated for later grouping
        indicators = list(map(
            lambda v: {
                **v,
                'organic': organic, 'irrigated': irrigated,
                'country': impact.get('country'),
                'year': _impact_assessment_year(impact)
            }, impact.get('emissionsResourceUse', [])))
        indicators = reduce(_group_indicators, indicators, group[key]['indicators'])
        group[key]['indicators'] = indicators
        return group

    return reduce(group_by, impacts, {})


def _impact_assessment_year(impact: dict):
    date = safe_parse_date(impact.get('endDate'))
    return date.year if date else None


def _format_country_name(name: str):
    return re.sub(r'[\(\)\,\.\'\"]', '', unidecode(name).lower().replace(' ', '-')) if name else None


def _impact_assessment_id(n: dict, include_matrix=True):
    # TODO: handle impacts that dont have organic/irrigated version => only 1 final version
    return '-'.join(non_empty_list([
        n.get('product', {}).get('@id'),
        _format_country_name(n.get('country', {}).get('name')),
        n.get('startDate'),
        n.get('endDate'),
        ('organic' if n.get('organic', False) else 'conventional') if include_matrix else '',
        ('irrigated' if n.get('irrigated', False) else 'non-irrigated') if include_matrix else ''
    ]))


def _impact_assessment_name(n: dict, include_matrix=True):
    return ' - '.join(non_empty_list([
        n.get('product', {}).get('name'),
        n.get('country', {}).get('name'),
        ', '.join(non_empty_list([
            ('Organic' if n.get('organic', False) else 'Conventional') if include_matrix else '',
            ('Irrigated' if n.get('irrigated', False) else 'Non Irrigated') if include_matrix else ''
        ])),
        '-'.join([n.get('startDate'), n.get('endDate')])
    ]))


def _create_impact_assessment(data: dict):
    impact = {'type': SchemaType.IMPACTASSESSMENT.value}
    # copy properties from existing ImpactAssessment
    impact['startDate'] = data.get('startDate')
    impact['endDate'] = data.get('endDate')
    impact['product'] = linked_node(data['product'])
    impact['functionalUnitMeasure'] = data['functionalUnitMeasure']
    impact['functionalUnitQuantity'] = data['functionalUnitQuantity']
    impact['allocationMethod'] = data['allocationMethod']
    impact['systemBoundary'] = data['systemBoundary']
    impact['organic'] = data.get('organic', False)
    impact['irrigated'] = data.get('irrigated', False)
    impact['dataPrivate'] = False
    if data.get('country'):
        impact['country'] = data['country']
    if data.get('source'):
        impact['source'] = data['source']
    return impact


def _update_impact_assessment(country_name: str, start: int, end: int, source: dict = None, include_matrix=True):
    def update(impact: dict):
        impact['startDate'] = str(start)
        impact['endDate'] = str(end)
        country = _fetch_single(country_name) if isinstance(country_name, str) else country_name
        impact['country'] = linked_node({
            **country,
            '@type': SchemaType.TERM.value
        })
        impact['name'] = _impact_assessment_name(impact, include_matrix)
        impact['id'] = _impact_assessment_id(impact, include_matrix)
        return impact if source is None else {**impact, 'source': source}
    return update


def _remove_duplicated_impact_assessments(impacts: list):
    def filter_impact(impact: dict):
        # removes non-organic + non-irrigated original impacts (they are recalculated by country average)
        return impact.get('organic', False) or impact.get('irrigated', False) \
            or 'conventional-non-irrigated' not in impact.get('id')

    return list(filter(filter_impact, impacts))


def get_time_ranges(country_name: str, period_length=10):
    """
    Get time ranges starting from the earliest Impact to today.

    Parameters
    ----------
    country_name : str
        The country Name as found in the glossary to restrict the results by country.
    period_length : int
        Optional - length of the period, 10 by default.
        Example: with 10 year period and the earliest impact in 2006 returns [[2001, 2010], [2011, 2020], [2021, 2030]]

    Returns
    -------
    list
        A list of aggregations.
        Example: `[<impact_assesment1>, <impact_assesment2>]`
    """
    current_year = datetime.now().year
    # find the min year of existing impacts
    earliest_year = _earliest_impact_date(country_name)
    if earliest_year is None:
        logger.debug('No impacts found')
        return []
    earliest_year = int(earliest_year[0:4])
    min_year = round(math.floor(earliest_year / 10) * 10)
    max_year = round((math.floor(current_year / 10) + 1) * 10)
    logger.debug('Finding impacts between %s and %s', min_year, max_year)
    return [[i, i+period_length-1] for i in range(min_year, max_year, period_length)]
