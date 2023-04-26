import os
import re

import moz_sql_parser


def remove_null_condition(query):
    pattern = r"AND \w+ IS (NOT )?NULL"
    return re.sub(pattern, "", query)


def clean_query(content):
    # Check if content contains consecutive apostrophes
    cleaned_content = re.sub(r'(?<=\=)\s*(?=\'+)', '', content)  # remove space between = and ''
    cleaned_content = re.sub(r"(?<!\s=)(?<!=)''", '', cleaned_content)  # remove '' not preceded by = or space and =
    return cleaned_content


def correct_ILIKE_to_LIKE(query):
    updated_query = query.replace("ILIKE", "LIKE").replace("::interval", "")
    return updated_query


def create_file(directory, filename, content):
    # Create the directory if it doesn't already exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create the file path by joining the directory and filename
    file_path = os.path.join(directory, filename)

    # cleaned_content = remove_null_condition(cleaned_content)
    # cleaned_content = clean_query (cleaned_content)

    # Open the file in write mode and write the content to it
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"File {filename} created in directory {directory}")


def split_based_on_rel_number():
    # Set the path to the directory containing the files
    directory_path = "./cleaned/"

    # Loop over all the files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file is a file and not a directory
        if os.path.isfile(os.path.join(directory_path, filename)):
            # Open the file for reading
            with open(os.path.join(directory_path, filename), 'r', encoding="utf8") as file:
                # Read the contents of the file
                query = file.read()
                print(filename)
                ast = moz_sql_parser.parse(query)
                num_tables = len(ast["from"])
                print(num_tables)
                print(filename)
                create_file('queries_with_' + str(num_tables) + '_joined_tables/', filename, query)


def assign_table_aliases(from_clause, table_aliases):
    tables_with_no_aliases = set()

    for table in from_clause:
        if isinstance(table, str):
            tables_with_no_aliases.add(table)

    print(from_clause)
    print("tables with no aliases: ", tables_with_no_aliases)

    # Rewrite the query with aliases
    for table in from_clause:
        if isinstance(table, str):
            table_alias = table_aliases[table]
            table_index = from_clause.index(table)
            from_clause[table_index] = {'value': table, 'name': table_alias}

    return from_clause, tables_with_no_aliases


def replace_table_names_with_aliases_in_where_clause(where_clause, table_aliases, tables_with_no_aliases):
    if isinstance(where_clause, list):
        return [replace_table_names_with_aliases_in_where_clause(sub_clause, table_aliases, tables_with_no_aliases) for
                sub_clause
                in
                where_clause]
    elif isinstance(where_clause, dict):
        new_clause = {}
        for key, value in where_clause.items():
            if key == 'eq' or key == 'neq' or key == 'lt' or key == 'lte' or key == 'gt' or key == 'gte' or key == 'like' or key == 'nlike':

                if (isinstance(value[0], str) and '.' in value[0]) and (
                        isinstance(value[1], str) and '.' in value[1]):

                    left_new_value = value[0]
                    right_new_value = value[1]

                    left_table_name = value[0].split('.')[0]
                    if left_table_name in tables_with_no_aliases:
                        # print("clause before 00", where_clause[key])
                        left_new_value = f"{table_aliases[left_table_name]}.{value[0].split('.')[1]}"
                        new_clause[key] = [left_new_value, right_new_value]
                        # print("clause after 00", new_clause[key])
                    else:
                        new_clause[key] = [left_new_value, right_new_value]

                    right_table_name = value[1].split('.')[0]
                    if right_table_name in tables_with_no_aliases:
                        # print("clause before 01 ", where_clause[key])
                        right_new_value = f"{table_aliases[right_table_name]}.{value[1].split('.')[1]}"
                        new_clause[key] = [left_new_value, right_new_value]
                        # print("clause after 01", new_clause[key])
                    else:
                        new_clause[key] = [left_new_value, right_new_value]

                elif isinstance(value[0], str) and '.' in value[0]:
                    table_name = value[0].split('.')[0]
                    if table_name in tables_with_no_aliases:
                        # print("clause before 11", where_clause[key])
                        new_value = [f"{table_aliases[table_name]}.{value[0].split('.')[1]}", value[1]]
                        new_clause[key] = new_value
                        # print("clause after 11", new_value)
                    else:
                        new_clause[key] = value

                elif isinstance(value[1], str) and '.' in value[1]:
                    table_name = value[1].split('.')[0]
                    if table_name in tables_with_no_aliases:
                        # print("clause before 22 ", where_clause[key])
                        new_value = [value[0], f"{table_aliases[table_name]}.{value[1].split('.')[1]}"]
                        new_clause[key] = new_value
                        # print("clause after 22", new_clause[key])
                    else:
                        new_clause[key] = value
                else:
                    # print('else', value)
                    new_clause[key] = value
            else:
                new_clause[key] = replace_table_names_with_aliases_in_where_clause(value, table_aliases,
                                                                                   tables_with_no_aliases)
        return new_clause
    else:
        return where_clause


def replace_table_names_with_aliases_in_select_clause(select_clause, aliases, tables_with_no_aliases):
    def replace_value_with_alias(value):
        if isinstance(value, str) and '.' in value:
            left = value.split('.')[0]
            right = value.split('.')[1]
            print(left, right)
            if (left in tables_with_no_aliases):
                return f"{aliases[left]}.{right}"
            return value

        elif isinstance(value, dict):
            for k, v in value.items():
                value[k] = replace_value_with_alias(v)
        return value

    # when you have a single selection like: select count(distinct account.display_name)
    # select_clause is like this: {'value': {'count': {'distinct': {'value': 'account.display_name'}}}}
    if isinstance(select_clause, dict):
        select_clause = {'value': replace_value_with_alias(select_clause['value'])}
    # when you have multiple selection like: select count(distinct account.display_name), tag.name, comment.id
    # select_clause is like this:  [{'value': {'count': {'distinct': {'value': 'account.display_name'}}}},
    # {'value': 'tag.name'}, {'value': 'comment.id'}]
    elif isinstance(select_clause, list):
        for item in select_clause:
            item['value'] = replace_value_with_alias(item['value'])
    return select_clause


def replace_table_names_with_aliases(select_clause, table_aliases):
    def replace_value_with_alias(value):
        if isinstance(value, dict):
            if 'value' in value:
                value['value'] = replace_value_with_alias(value['value'])
            if 'name' in value and value['name'] not in table_aliases:
                value['name'] = table_aliases.get(value['name'], value['name'])
        elif isinstance(value, list):
            value = [replace_value_with_alias(v) for v in value]
        return value

    if isinstance(select_clause, list):
        for item in select_clause:
            item['value'] = replace_value_with_alias(item['value'])
    elif isinstance(select_clause, dict):
        select_clause['value'] = replace_value_with_alias(select_clause['value'])

    return select_clause


if __name__ == '__main__':
    table_aliases = {'account': 'acc', 'so_user': 'u', 'tag': 't', 'comment': 'c', 'site': 's', 'tag_question': 'tq',
                     'answer': 'a', 'question': 'q', 'post_link': 'pl', 'badge': 'b'}

    # Set the path to the directory containing the files
    directory_path = "queries_with_6_joined_tables"

    # Loop over all the files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file is a file and not a directory
        if os.path.isfile(os.path.join(directory_path, filename)) :
            # Open the file for reading
            with open(os.path.join(directory_path, filename), 'r', encoding="utf8") as file:
                # Read the contents of the file
                query = file.read()
                print("query read: " , filename)
                parsed_query = moz_sql_parser.parse(query)

                select_clause = parsed_query['select']
                from_clause = parsed_query['from']
                where_clause = parsed_query['where']
                # print(select_clause)

                new_from_clause, tables_with_no_aliases = assign_table_aliases(from_clause, table_aliases)
                new_where_clause = replace_table_names_with_aliases_in_where_clause(where_clause, table_aliases,
                                                                                    tables_with_no_aliases)
                new_select_clause = replace_table_names_with_aliases_in_select_clause(select_clause, table_aliases,
                                                                                      tables_with_no_aliases)

                parsed_query['select'] = new_select_clause
                parsed_query['from'] = new_from_clause
                parsed_query['where'] = new_where_clause

                rewritten_query = moz_sql_parser.format(parsed_query)

                create_file('cleaned_with_aliases_6_joined', filename, rewritten_query)
