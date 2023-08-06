from pkgutil import extend_path
from concurrent.futures import ThreadPoolExecutor
from hestia_earth.utils.tools import current_time_ms, flatten

from .log import logger
from .utils.term import DEFAULT_COUNTRY_NAME, _fetch_default_country, _fetch_single
from .utils.source import _get_source
from .utils.impact_assessment import (
    get_time_ranges, _all_impacts_by_product, _global_impacts_by_product,
    _update_impact_assessment, _remove_duplicated_impact_assessments
)
from .models.terms import aggregate as aggregate_by_term
from .models.countries import aggregate as aggregate_by_country
from .models.world import aggregate as aggregate_world

__path__ = extend_path(__path__, __name__)


def _aggregate_by_term(start_year: int, end_year: int, country=dict) -> list:
    impacts = _all_impacts_by_product(start_year, end_year, country.get('name'))
    source = _get_source()
    impacts = aggregate_by_term(impacts)
    return list(map(_update_impact_assessment(country, start_year, end_year, source), impacts))


def _aggregate_by_country(start_year: int, end_year: int, country_name=str) -> list:
    country = _fetch_single(country_name)
    if country is None:
        raise Exception('Country not found: ' + country_name)

    now = current_time_ms()

    # step 1: aggregate all impacts indexed on the platform
    impacts = _aggregate_by_term(start_year, end_year, country)

    # step 2: use aggregated impacts to calculate country-level impacts
    impacts = aggregate_by_country(impacts)

    # step 3: remove duplicates for product without matrix organic/irrigated
    impacts = _remove_duplicated_impact_assessments(impacts)

    logger.info('time=%s, unit=ms', current_time_ms() - now)

    return impacts


def _aggregate_global(start_year: int, end_year: int) -> list:
    now = current_time_ms()

    impacts = _global_impacts_by_product(start_year, end_year)
    source = _get_source()
    country = _fetch_default_country()

    impacts = aggregate_world(impacts)
    impacts = list(map(_update_impact_assessment(country, start_year, end_year, source, False), impacts))

    logger.info('time=%s, unit=ms', current_time_ms() - now)

    return impacts


def aggregate(country_name=DEFAULT_COUNTRY_NAME):
    """
    Aggregates data from Hestia.
    Produced data will be aggregated by country or globally if no `country_name` is provided.

    Parameters
    ----------
    country_name : str
        Optional - the country Name as found in the glossary to restrict the results by country.
        Returns aggregations for the world by default if not provided.

    Returns
    -------
    list
        A list of aggregations.
        Example: `[<impact_assesment1>, <impact_assesment2>]`
    """
    def run(time_range):
        [start_year, end_year] = time_range
        is_global = country_name is None or country_name == DEFAULT_COUNTRY_NAME
        return _aggregate_global(start_year, end_year) if is_global \
            else _aggregate_by_country(start_year, end_year, country_name)

    with ThreadPoolExecutor() as executor:
        return flatten(executor.map(run, get_time_ranges(country_name)))
