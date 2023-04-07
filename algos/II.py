from algos.helper_functions import connect_bdd
import moz_sql_parser
import itertools


def iterative_improvement(query, num_permutations ):

    # Parse the query and extract the table names
    parsed_query = moz_sql_parser.parse(query)
    tables = parsed_query['from']

    # Initialize the best join order and its cost
    best_join_order = tables.copy()
    best_cost = get_join_order_cost(parsed_query, best_join_order)

    # Loop over all possible starting join orders
    index = 0
    for starting_join_order in itertools.islice(itertools.permutations(tables), num_permutations):
        index += 1
        print("mother loop index", index)
        # Initialize the current join order and its cost
        current_join_order = list(starting_join_order)
        current_cost = get_join_order_cost(parsed_query, current_join_order)


        # Generate all possible adjacent join orders
        neighbors = neighborhood(current_join_order)

        improved = False
        # Evaluate the cost of each neighbor
        for neighbor in neighbors:

                neighbor_cost = get_join_order_cost(parsed_query, neighbor)

                # If the neighbor has a lower cost, select it as the new join order
                if neighbor_cost < current_cost:
                    current_join_order = neighbor.copy()
                    current_cost = neighbor_cost
                    print("current neighbor_cost: ", neighbor_cost)

                    # If the new join order is better than the best seen so far, update it
                    if current_cost < best_cost:
                        improved = True
                        best_join_order = current_join_order.copy()
                        best_cost = current_cost
                        print("current best_cost: ", best_cost)
                if(improved):
                    break
        # if(improved):
        #     break

    # Reconstruct the query with the best join order
    parsed_query['from'] = best_join_order
    print("best join order: ", best_join_order)
    optimal_query = moz_sql_parser.format(parsed_query)

    return optimal_query , best_cost


# Define the neighborhood function that generates adjacent join orders
def neighborhood(join_order):
        neighbors = []
        for i in range(len(join_order) - 1):
            for j in range(i + 1, len(join_order)):
                neighbor = join_order.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)
        return neighbors


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

    cursor.execute("explain (format json) "+modified_query)
    file=cursor.fetchone()[0][0]
    result=file['Plan']["Total Cost"]

    return result
