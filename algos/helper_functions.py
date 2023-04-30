import os
import random

import moz_sql_parser
import numpy as np
import psycopg2
from moz_sql_parser import parse

joinedTables = []
joinedClauses = []
alias = {}


def init():
    global joinedTables
    joinedTables = []
    global joinedClauses
    joinedClauses = []
    global alias
    alias = {}


def queryParser(input):
    init()

    parsed_query = parse(input)
    from_clause = parsed_query["from"]

    for j in range(0, len(from_clause)):
        joinedTables.append(from_clause[j]["value"])
        alias[from_clause[j]["name"]] = from_clause[j]["value"]

    where_clause = parsed_query["where"]["and"]
    k = 0
    while k < len(where_clause):
        if "eq" in where_clause[k]:
            if isinstance(where_clause[k]['eq'][1], str):
                joinedClauses.append(where_clause[k]['eq'])
                where_clause.remove(where_clause[k])
            else:
                k += 1
        else:
            k += 1

    return joinedTables, parsed_query, alias


def get_cost(query):
    conn, cursor = connect_bdd("stack")

    cursor.execute("explain (format json) " + query)
    file = cursor.fetchone()[0][0]
    result = file['Plan']["Total Cost"]

    disconnect_bdd(conn)
    return result


def get_query_latency(query, force_order):
    conn, cursor = connect_bdd("stack")
    # Prepare query
    join_collapse_limit = "SET join_collapse_limit ="
    join_collapse_limit += "1" if force_order else "8"
    query = join_collapse_limit + "; EXPLAIN  ANALYSE " + query + ";"

    cursor.execute(query)

    rows = cursor.fetchall()
    row = rows[0][0]
    latency = float(rows[0][0].split("actual time=")[1].split("..")[1].split(" ")[0])

    disconnect_bdd(conn)
    return latency


def get_solution_cost(query):
    conn, cursor = connect_bdd("stack")
    cursor.execute("SET join_collapse_limit =1;")

    cursor.execute("explain (format json) " + query)
    file = cursor.fetchone()[0][0]
    result = file['Plan']["Total Cost"]
    disconnect_bdd(conn)

    return result


def get_pg_cost(query):
    conn, cursor = connect_bdd("stack")

    cursor.execute("explain (format json) " + query)
    file = cursor.fetchone()[0][0]
    result = file['Plan']["Total Cost"]
    disconnect_bdd(conn)

    return result

def connect_bdd(name):
    conn = psycopg2.connect(host="localhost",
                            user="postgres", password="postgres",
                            database=name)
    cursor = conn.cursor()
    return [conn, cursor]


def disconnect_bdd(conn):
    conn.close()


def get_tableWithSelectivity(parsed_query):
    result = {}
    where_clause = parsed_query["where"]["and"]
    for k in range(0, len(where_clause)):
        if "or" in where_clause[k]:
            print("ddddd", where_clause[k])
            table = list(list(where_clause[k].values())[0][0].values())[0][0].rpartition('.')[0]
            if (table not in result):
                result[table] = [where_clause[k]]
            else:
                result[table].append(where_clause[k])

        else:
            table = list(where_clause[k].values())[0][0].rpartition('.')[0]
            if (table not in result):
                result[table] = [where_clause[k]]
            else:
                result[table].append(where_clause[k])

    return result


def get_modified_query(parsed_query, join_order):
    # Replace the 'FROM' clause with the specified join order
    parsed_query['from'] = join_order

    # Generate the modified SQL query from the AST
    modified_query = moz_sql_parser.format(parsed_query)

    return modified_query


def get_join_order_cost(parsed_query, join_order):

    modified_query = get_modified_query(parsed_query, join_order)

    conn, cursor = connect_bdd("imdbload")
    cursor.execute("SET join_collapse_limit = 1;")
    cursor.execute("explain (format json) " + modified_query)
    file = cursor.fetchone()[0][0]
    result = file['Plan']["Total Cost"]

    disconnect_bdd(conn)
    return result


def create_file(directory, filename, content):
    # Create the directory if it doesn't already exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create the file path by joining the directory and filename
    file_path = os.path.join(directory, filename)

    # Open the file in write mode and write the content to it
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"File {filename} created in directory {directory}")



# Define the neighborhood function that generates adjacent join orders
def neighborhood(join_order):
        neighbors = []
        for i in range(len(join_order) - 1):
            for j in range(i + 1, len(join_order)):
                neighbor = join_order.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)
        return neighbors