import random
import string
from postgrest.table_names import TableNames


def generate_random_string():
    # Credit: https://stackoverflow.com/a/2257449
    str_length = 8
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=str_length))


def get_column_metadata_table_name_for_table(table_name: str):
    """Returns the table name used for a given table's column metadata.
    Mostly applies to the "application_new" and "capacity_new" tables.
    """
    if table_name == TableNames.CAPACITY_NEW:
        # Column metadata table name should be "CAPACITY"
        # but the wizard fields should come from "CAPACITY_NEW".
        return TableNames.CAPACITY
    elif table_name == TableNames.APPLICATION_NEW:
        # Column metadata table name should be "APPLICATION"
        # but the wizard fields should come from "APPLICATION_NEW".
        return TableNames.APPLICATION
    return table_name