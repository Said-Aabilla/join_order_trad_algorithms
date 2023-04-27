
import moz_sql_parser

def convert_to_explicit_join(query):
    from moz_sql_parser import parse, format


    new_from = ''

    parsed_query = parse(query)
    aliases_map = {}
    table_names = [table['value'] for table in parsed_query['from']]
    table_aliases = [table['name'] for table in parsed_query['from']]
    for index, alias in enumerate(table_aliases):
        table = table_names[index]
        aliases_map[alias] = table

    join_conditions = parsed_query['where']['and']
    join_order = []
    helper_to_alter_where = []
    # create explicit join conditions
    i = 0
    for condition in join_conditions:
        # print(i)
        if 'eq' in condition and '.' in condition['eq'][0] and '.' in condition['eq'][1]:
            i = i + 1
            print(condition)

            left = condition['eq'][0].split('.')[0]
            right = condition['eq'][1].split('.')[0]
            if left in table_aliases and right in table_aliases and i == 1:

                new_from += f" FROM {aliases_map[left]} AS {left} JOIN {aliases_map[right]} AS {right} ON {condition['eq'][0]} = {condition['eq'][1]}"
                join_order.append(aliases_map[left])
                join_order.append(aliases_map[right])

            elif left in table_aliases and right in table_aliases and (i != 1):
                if aliases_map[right] in join_order and aliases_map[left] in join_order:
                    last_joined = join_order[-1]
                    print("last_joined : ", last_joined)
                    if last_joined == aliases_map[right]:
                        new_from += f" And  {condition['eq'][0]} = {condition['eq'][1]}"
                    elif last_joined == aliases_map[left]:
                        new_from += f" And  {condition['eq'][0]} = {condition['eq'][1]}"

                elif aliases_map[right] in join_order:
                    new_from += f" JOIN {aliases_map[left]} AS {left} ON {condition['eq'][0]} = {condition['eq'][1]}"
                    join_order.append(aliases_map[left])

                elif aliases_map[left] in join_order:
                    new_from += f" JOIN {aliases_map[right]} AS {right} ON {condition['eq'][0]} = {condition['eq'][1]}"
                    join_order.append(aliases_map[right])
        else:
            helper_to_alter_where.append(condition)

    # get only SELECT statement
    idx = query.index("FROM")
    select_stmt = query[:idx]
    print("new selecet:", select_stmt)

    # new_where
    parsed_query['where']['and'] = helper_to_alter_where
    new_query_with_updated_where = format(parsed_query)
    idx = new_query_with_updated_where.index("WHERE")
    where_stmt = new_query_with_updated_where[idx:]
    print("new where_stmt:", where_stmt)

    return f'{select_stmt} {new_from} {where_stmt}'


if __name__ == '__main__':
    query = "SELECT MIN(mc.note) AS production_note, MIN(t.title) AS movie_title, MIN(t.production_year) AS movie_year FROM company_type AS ct, info_type AS it, movie_companies AS mc, movie_info_idx AS mi_idx, title AS t WHERE ct.kind = 'production companies' AND it.info = 'top 250 rank' AND mc.note NOT LIKE '%(as Metro-Goldwyn-Mayer Pictures)%' AND (mc.note LIKE '%(co-production)%' OR mc.note LIKE '%(presents)%') AND ct.id = mc.company_type_id AND t.id = mc.movie_id AND t.id = mi_idx.movie_id AND mc.movie_id = mi_idx.movie_id AND it.id = mi_idx.info_type_id;"
    explicit_join_query = convert_to_explicit_join(query)
    print(explicit_join_query)
