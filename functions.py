import re


# Function to generate email based on the student name
def generate_email(name):
    # Remove special characters
    clean_name = re.sub(r"[^a-zA-Z ]", "", name)
    name_parts = clean_name.split()

    if len(name_parts) == 1:
        email = f"{name_parts[0].lower()}@gmail.com"
    else:
        email = f"{name_parts[0][0].lower()}{name_parts[-1].lower()}@gmail.com"

    return email


# Function to find names with special characters
def find_names_with_special_characters(names_list):
    special_names = [name for name in names_list if re.search(r"[^a-zA-Z ]", name)]
    return special_names

