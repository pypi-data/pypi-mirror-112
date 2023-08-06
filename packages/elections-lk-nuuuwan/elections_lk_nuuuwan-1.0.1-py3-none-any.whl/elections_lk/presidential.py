"""Implements presidential."""
import os

from utils import ds, timex, www
from utils.cache import cache

from elections_lk._constants import CACHE_NAME, CACHE_TIMEOUT
from elections_lk._utils import log


def get_election_years():
    """Implement presidential."""
    return [
        1982,
        1988,
        1994,
        1999,
        2005,
        2010,
        2015,
        2019,
    ]


def _clean_by_party(by_party):
    return {
        'party_id': by_party['party_code'],
        'votes': (int)(by_party['votes']),
    }


def _clean_pd_result(pd_result):
    cleaned_result = {}
    cleaned_result['ed_id'] = 'EC-' + pd_result['ed_code']
    cleaned_result['pd_id'] = 'EC-' + pd_result['pd_code']
    cleaned_result['ed_name'] = pd_result['ed_name']
    cleaned_result['pd_name'] = pd_result['pd_name']
    cleaned_result['time_ut'] = pd_result['timestamp']
    cleaned_result['time'] = timex.format_time(
        pd_result['timestamp'],
        '%Y-%m-%d %H:%M:%S',
    )

    cleaned_result['by_party'] = sorted(
        list(
            map(
                _clean_by_party,
                pd_result['by_party'],
            )
        ),
        key=lambda for_party: -for_party['votes'],
    )

    cleaned_result['summary'] = {
        'valid': pd_result['summary']['valid'],
        'rejected': pd_result['summary']['rejected'],
        'polled': pd_result['summary']['polled'],
        'electors': pd_result['summary']['electors'],
    }

    return cleaned_result


@cache(CACHE_NAME, CACHE_TIMEOUT)
def get_election_data(year):
    url = os.path.join(
        'https://raw.githubusercontent.com',
        'nuuuwan/elections_lk/data',
        'elections_lk.presidential.%d.json' % year,
    )
    log.info('Downloading data from %s', url)
    all_results = www.read_json(url)
    pd_results = list(
        filter(
            lambda result: result['level'] == 'POLLING-DIVISION',
            all_results,
        )
    )
    cleaned_pd_results = sorted(
        list(
            map(
                _clean_pd_result,
                pd_results,
            )
        ),
        key=lambda result: result['time_ut'],
    )
    return cleaned_pd_results


def get_party_result(result, party_id):
    """Get party result."""
    for_partys = list(
        filter(
            lambda d: d['party_id'] == party_id,
            result['by_party'],
        )
    )
    return for_partys[0] if len(for_partys) == 1 else None


def get_winning_party_info(result):
    """Get winning party result."""
    return result['by_party'][0]


def get_election_data_index(year):
    """Get election data, indexed by PD."""
    return ds.dict_list_to_index(get_election_data(year), 'pd_id')
