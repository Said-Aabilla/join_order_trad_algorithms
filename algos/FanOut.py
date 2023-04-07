from algos.helper_functions import *


tablesWithSel = {}
sortedTables = []


def FanOut(input, cursor):
    state = []
    solution = {}
    query = "select count(*) from " + FACT
    print("query", query)
    cursor.execute(query)
    factCar = cursor.fetchall()[0][0]
    # calculer les cardinalités des tables
    joinedTables, parsed_query, alias = queryParser(input)
    print(alias)
    joinedTables.remove(FACT)
    print(joinedTables)
    tables = get_tableWithSelectivity(parsed_query)
    print(tables)

    print(tables.keys())

    for key in tables.keys():
        print(tables.keys())
        json = {'select': {'value': {'count': '*'}}, 'from': [{'value': 'lineorder', 'name': 'l'},
                                                              {'left join': {'name': key, 'value': alias[key]},
                                                               'on': {'eq': get_joinedClause(alias[key])}}]}
        if len(tables[key]) == 1:
            json['where'] = tables[key][0]
        else:
            json['where'] = {'and': tables[key]}
        query = format(json)
        print("query", query)
        cursor.execute(query)
        tablesWithSel[alias[key]] = cursor.fetchall()[0][0] / factCar
    print("tablewithsel", tablesWithSel)
    if (len(joinedTables) > len(tablesWithSel)):
        for t in joinedTables:
            if t not in tablesWithSel:
                query = "select count(*) from lineorder l left join " + t + " as " + get_key(t, alias) + " on " + \
                        get_joinedClause(t)[0] + " = " + get_joinedClause(t)[1]
                print("query", query)
                cursor.execute(query)
                tablesWithSel[t] = cursor.fetchall()[0][0] / factCar

    sortedTables = {k: v for k, v in sorted(tablesWithSel.items(), key=lambda item: item[1])}
    state = list(sortedTables.keys())
    state.insert(1, FACT)
    print(state)
    solution["query"] = listToQuery(state, get_indice(state), parsed_query)
    solution["runTime"] = get_runTime(solution["query"], cursor)
    solution["solutionCost"] = get_solution_cost(solution["query"])
    solution["postgresCost"] = get_cost(input)

    return solution

