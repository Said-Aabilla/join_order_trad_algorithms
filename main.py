import json

import requests

BASE_URL = 'http://127.0.0.1:8000'
headers = {'content-type': 'application/json'}

def get_table_id(table_name):
    url = f'{BASE_URL}/tables/{table_name}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['table_id']
    else:
        return None


def get_attribute_id(attribute_name, table_name):
    url = f'{BASE_URL}/tables/{table_name}/attributes/{attribute_name}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['attribute_id']
    else:
        return None

def create_query(query_str, table_ids, selection_info=[], projection_info=[], join_info=[]):
    data = {'query': query_str, 'table': table_ids, 'selection': selection_info, 'projection': projection_info,
            'join': join_info}

    response = requests.post(BASE_URL + '/queries', data=json.dumps(data), headers=headers)

    if response.status_code == 201:
        query_id = response.json()['id']
        return query_id
    else:
        return None

import json
from moz_sql_parser import parse



def parse_sql_query(sql_query):

    alias_name_2_table_name = {'kt1': 'kind_type', 'chn': 'char_name', 'cn1': 29, 'mi_idx2': 'movie_info_idx', 'cct1': 23, 'n': 21, 'a1': 39, 'kt2': 32, 'miidx': 'movie_info_idx', 'it': 16, 'mi_idx1': 35, 'kt': 17, 'lt': 9, 'ci': 2, 't': 'title', 'k': 'keyword',  'ml': 11, 'ct': 4, 't2': 28, 'rt': 6, 'it2': 13, 'an1': 37, 'at': 19, 'mc2': 34, 'pi': 26, 'mc': 5, 'mi_idx': 'movie_info_idx', 'n1': 38, 'cn2': 30, 'mi': 14, 'it1': 12, 'cc': 22, 'cct2': 24, 'an': 20, 'mk': 10, 'cn': 3, 'it3': 25, 't1': 27, 'mc1': 33}

    parsed_query = parse(sql_query)

    # Extract necessary elements from the parsed query
    query = parsed_query['select']
    parsed_tables = parsed_query['from']
    tables={}
    where_clause = parsed_query.get('where')
    join_clause = parsed_query.get('join')

    # Create the JSON object
    json_object = {
        "query": "sql_query",
        "tables": [],
        "selections": [],
        "projections": [],
        "joins": []
    }

    # Add table IDs to the JSON object
    for table in parsed_tables:
        print(table['value'])
        table_id = get_table_id(table['value'])
        if table_id:
            json_object['tables'].append(table_id)

    # Extract selections
    if isinstance(query, dict):
        for attribute, alias in query.items():
            if isinstance(alias, dict) and 'literal' in alias:
                attribute_id = get_attribute_id(json_object['table'][0], attribute)
                json_object['selection'].append(attribute_id)
            else:
                attribute_id = get_attribute_id(json_object['table'][0], alias)
                json_object['selection'].append(attribute_id)

    return json_object


if __name__ == '__main__':

   query = "SELECT MIN(mc.note) AS production_note, MIN(t.title) AS movie_title, MIN(t.production_year) AS movie_year FROM company_type AS ct, info_type AS it, movie_companies AS mc, movie_info_idx AS mi_idx, title AS t WHERE ct.kind = 'production companies' AND it.info = 'top 250 rank' AND mc.note NOT LIKE '%(as Metro-Goldwyn-Mayer Pictures)%' AND (mc.note LIKE '%(co-production)%' OR mc.note LIKE '%(presents)%') AND ct.id = mc.company_type_id AND t.id = mc.movie_id AND t.id = mi_idx.movie_id AND mc.movie_id = mi_idx.movie_id AND it.id = mi_idx.info_type_id;"

   result = parse_sql_query(query)

   print(result)