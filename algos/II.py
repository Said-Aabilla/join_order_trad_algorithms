from algos.SA import get_join_conds
from algos.helper_functions import get_join_order_cost, neighborhood, get_modified_query
import moz_sql_parser
import itertools


def iterative_improvement(query, num_permutations,filename ):

    # Parse the query and extract the table names
    parsed_query = moz_sql_parser.parse(query)
    tables = parsed_query['from']

    # Initialize the best join order and its cost
    best_join_order = get_join_conds(parsed_query)
    try:
        best_cost = get_join_order_cost(query, best_join_order)
    except:
        best_cost = float('inf')

    print(f"-------init------------------------------{best_cost}--")

    # Loop over all possible starting join orders
    index = 0
    for starting_join_order in itertools.islice(itertools.permutations(tables), num_permutations):
        index += 1
        # print("mother loop index", index)
        # Initialize the current join order and its cost
        current_join_order = list(starting_join_order)
        try:
            current_cost = get_join_order_cost(query, current_join_order)
        except:
            current_cost = float('inf')

        # Generate possible adjacent join orders
        neighbors = neighborhood(current_join_order)

        improved = False
        # Evaluate the cost of each neighbor
        for neighbor in neighbors:

                try:
                    neighbor_cost = get_join_order_cost(query, neighbor)
                except:
                    neighbor_cost =  float('inf')
                    print(f"--------------------------------------------{filename}-----------------------------------------------")
                    continue


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
                        print("best_cost: ", best_cost)
                if(improved):
                    break
        # if(improved):
        #     break

    # Reconstruct the query with the best join order
    # parsed_query['from'] = best_join_order
    # print("best join order: ", best_join_order)
    optimal_query, join_order = get_modified_query(query, best_join_order)

    return optimal_query, best_cost , join_order


