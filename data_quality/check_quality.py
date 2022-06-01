import pandas as pd
import logging


def log_duplicates_in_column(df: pd.DataFrame, column_list: list):
    """A function to check for duplicates in a list of columns.

    Args:
        df (pd.DataFrame): dataframe on which to perform quality checks.
        column_list (list): list of columns that might contain duplicates.
    """

    for column in column_list:

        duplicated_values_count = len(df[df[[f"{column}"]].duplicated(subset=[f"{column}"])])

        logging.info(
            f"There are {duplicated_values_count} duplicated values in {column} column."
        )
    

def check_data_quality(df: pd.DataFrame) -> None:
    """Wrapper function that logs checks data quality.

    Args:
        df (_type_): Dataframe on which to perform quality checks.
    """

    log_duplicates_in_column(df, ["policy_id"])
    logging.info(f"There are {len(df[df.duplicated()])} dupicated rows.")
    logging.info(f"Missing values summary: \n { pd.DataFrame(df.isna().sum())} ")
    logging.info(f"Data set description: \n {df.describe()}")

    return