
import os
import re

def remove_null_condition(query):
    pattern = r"AND \w+ IS (NOT )?NULL"
    return re.sub(pattern, "", query)

def create_file(directory, filename, content):
    # Create the directory if it doesn't already exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create the file path by joining the directory and filename
    file_path = os.path.join(directory, filename)

    # Check if content contains consecutive apostrophes
    cleaned_content = re.sub(r'(?<=\=)\s*(?=\'+)', '', content)  # remove space between = and ''
    cleaned_content = re.sub(r"(?<!\s=)(?<!=)''", '', cleaned_content)  # remove '' not preceded by = or space and =

    # cleaned_content = remove_null_condition(cleaned_content)

    # Open the file in write mode and write the content to it
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"File {filename} created in directory {directory}")


def remove_null_condition(query):
    pattern = r"AND \S+? IS (NOT )?NULL"
    # print(f"Before replacement:\n{query}\n")
    result = re.sub(pattern, "", query)
    # print(f"After replacement:\n{result}\n")
    return result




def correct_ILIKE_to_LIKE(query):
    updated_query =query.replace("ILIKE", "LIKE").replace("::interval", "")
    return updated_query

if __name__ == '__main__':

    # Set the path to the directory containing the files
    directory_path = "./all/"


    # Loop over all the files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file is a file and not a directory
        if os.path.isfile(os.path.join(directory_path, filename)):
            # Open the file for reading
            with open(os.path.join(directory_path, filename), 'r', encoding="utf8") as file:
                # Read the contents of the file
                query = file.read()
                updated_query= correct_ILIKE_to_LIKE(query)

        create_file("cleaned", filename,updated_query)
