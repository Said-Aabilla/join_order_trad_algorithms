import moz_sql_parser

from algos.SA import get_join_conds
from algos.helper_functions import *

alias_map = {"char_name": ["chn"], "cast_info": ["ci"], "company_name": ["cn", "cn1", "cn2"], "company_type": ["ct"],
             "movie_companies": ["mc", "mc1", "mc2"], "role_type": ["rt"], "title": ["t", "t1", "t2"], "keyword": ["k"],
             "link_type": ["lt"], "movie_keyword": ["mk"], "movie_link": ["ml"], "movie_info": ["mi"],
             "movie_info_idx": ["mi_idx", "mi_idx2", "mi_idx1", "miidx"], "kind_type": ["kt", "kt1", "kt2"],
             "aka_title": ["at"], "aka_name": ["an", "an1"], "complete_cast": ["cc"],
             "comp_cast_type": ["cct1", "cct2"], "info_type": ["it", "it1", "it2"], "person_info": ["pi"],
             "name": ["n1", "n"]}

tablesWithSel = {}
sortedTables = []


def min_selectivity(input, cursor, my_tables):
    state = []
    solution = {}
    joinedTables, parsed_query, alias = queryParser(input)

    tables = get_tableWithSelectivity(parsed_query)

    # calculate selectivity
    for key in tables.keys():
        json = {'select': {'value': {'count': '*'}}, 'from': {'value': alias[key], 'name': key}}
        if len(tables[key]) == 1:
            json['where'] = tables[key][0]
        else:
            json['where'] = {'and': tables[key]}
        query = moz_sql_parser.format(json)

        print("query: ", query)
        cursor.execute(query)
        tablesWithSel[alias[key]] = cursor.fetchall()[0][0]

    # add tables without selectivity
    if len(joinedTables) > len(tablesWithSel):
        for t in joinedTables:
            if t not in tablesWithSel:
                tablesWithSel[t] = my_tables[t]

    sortedTables = {k: v for k, v in sorted(tablesWithSel.items(), key=lambda item: item[1])}
    state = list(sortedTables.keys())

    my_parsed_query = moz_sql_parser.parse(input)

    default_join_order = get_join_conds(my_parsed_query)

    hint = reorder_join_conditions(state, default_join_order)

    hint_str = f" /*+ Leading ({'  '.join(hint)}) */ "
    input = f"{hint_str}  {input}"

    return input


def reorder_join_conditions(state, default_join_order):
    new_order = []
    for table in state:
        for condition in default_join_order:
            left = condition['eq'][0].split('.')[0]
            right = condition['eq'][1].split('.')[0]
            if right in alias_map[table] and right not in new_order:
                new_order.append(right)
            elif left in alias_map[table] and left not in new_order:
                new_order.append(left)
            else:
                continue
    return new_order
