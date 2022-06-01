import pandas as pd
import logging


def log_duplicates_in_column(df, column_list):

    for column in column_list:

        duplicated_values_count = len(df[df[[f"{column}"]].duplicated(subset=[f"{column}"])])

        logging.info(
            f"There are {duplicated_values_count} duplicated values in {column} column."
        )

    return
    

def check_data_quality(df):

    log_duplicates_in_column(df, ["policy_id"])
    logging.info(f"There are {len(df[df.duplicated()])} dupicated rows.")
    logging.info(f"Missing values summary: \n { pd.DataFrame(df.isna().sum())} ")
    logging.info(f"Data set description: \n {df.describe()}")

    return