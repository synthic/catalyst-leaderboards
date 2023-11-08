import json
from pathlib import Path

import requests

platforms = ['pc', 'ps4', 'xboxone']

dashes = [
    'ch_rrt_tv2_time',
    'ch_rrt_tv04_time',
    'ch_rrt_dt4_time',
    'ch_rrt_tv3_time',
    'ch_rrt_anc1_time',
    'ch_rrt_dt1_time',
    'ch_rrt_rz3_time',
    'ch_rrt_tv05_time',
    'ch_rrt_dt2_time',
    'ch_rrt_rz4_time',
    'ch_rrt_dt3_time',
    'ch_rrt_anc4_time',
    'ch_rrt_anc5_time',
    'ch_rrt_bm1_time',
    'ch_rrt_anc6_time',
    'ch_rrt_tv1_time',
    'ch_rrt_dt6_time',
    'ch_rrt_anc2_time',
    'ch_rrt_rz2_time',
    'ch_rrt_anc3_time',
    'ch_rrt_dt5_time',
    'ch_rrt_rz1_time'
]

def get_leaderboard(dash, offset=None):
    response = requests.post(api, json={
        'jsonrpc': '2.0',
        'method': 'Pamplona.getRunnersRouteLeaderboard',
        'params': {
            'challengeId': dash,
            'offset': offset,
            'count': None
        }
    })

    return response.json()

for platform in platforms:
    api = 'https://mec-gw.ops.dice.se/jsonrpc/prod_default/prod_default/' + platform + '/api'

    for dash in dashes:
        # Get total entries in leaderboard
        data = get_leaderboard(dash)
        total = data['result']['leaderboard']['totalCount']

        print(dash)

        offset = 0
        result = []

        # Fetch data and append to list
        while offset < total:
            data = get_leaderboard(dash, offset)
            result += data['result']['leaderboard']['users']

            print(str(len(result)) + '/' + str(total), end='\r')

            offset += 100

        print('\n')

        # Output json file
        p = (Path(__file__).parent).joinpath('leaderboards', platform)
        p.mkdir(parents=True, exist_ok=True)

        with open(p.joinpath(dash + '.json'), 'w', encoding='utf-8', newline='\n') as f:
            json.dump(result, f, indent=4)
