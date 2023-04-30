import json

import requests

BASE_URL = 'http://127.0.0.1:8000'
headers = {'content-type': 'application/json'}


def create_query(query_str, table_ids, selection_info=[], projection_info=[], join_info=[]):
    data = {'query': query_str, 'table': table_ids, 'selection': selection_info, 'projection': projection_info,
            'join': join_info}

    response = requests.post(BASE_URL + '/queries', data=json.dumps(data), headers=headers)

    if response.status_code == 201:
        query_id = response.json()['id']
        return query_id
    else:
        return None


