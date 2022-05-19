import datetime
import numpy as np
import pandas as pd


def calculate_car_age(df: pd.DataFrame) -> pd.DataFrame:
    """Given year of car, calculates car age.

    Args:
        df (pd.DataFrame): car year registration column.

    Returns:
        pd.DataFrame: a dataframe with one car_age column
    """
    df = df.copy()
    df["car_age"] = datetime.datetime.now() - pd.to_datetime(df, format="%Y")
    df["car_age"] = (df["car_age"] / np.timedelta64(1, "Y")).astype("float").round(1)

    return df


def calculate_exposure(
    df: pd.DataFrame, policy_start_column_name: str, policy_end_column_name: str
) -> pd.DataFrame:
    """Calculates car exposure.

    Args:
        df (pd.DataFrame): dataframe with policy start and ending columns.
        policy_start_column_name (str): name of policy start column.
        policy_end_column_name (str): name of policy end column.

    Returns:
        pd.DataFrame: the same dataframe with additional exposure column.
    """
    df["exposure"] = (
        df[f"{policy_end_column_name}"] - df[f"{policy_start_column_name}"]
    ) / np.timedelta64(1, "Y")
    df["exposure"] = df["exposure"].astype("float")

    return df
