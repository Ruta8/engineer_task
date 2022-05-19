import pandas as pd
import numpy as np
import dateutil.parser as parser

from utils.get_data import combine_files, get_file_list

from utils.process_data import calculate_car_age, calculate_exposure


def program():

    # Get data
    file_list = get_file_list(data_path="data/raw/", file_names_start_with="task_data")

    combined_files = combine_files(file_list)

    combined_files.to_csv("data/processed/task_data.csv", index=False)
    policy_data = pd.read_csv("data/external/POLICY_DATA.csv")

    df = combined_files.merge(policy_data, how="left", on="policy_id")

    # Fill in missing
    df["car_brand"].fillna(df["car_brand"].mode(), inplace=True)
    df["postal_code"].fillna(df["postal_code"].mode(), inplace=True)
    df[["car_eng_pow", "customer_age"]] = df[["car_eng_pow", "customer_age"]].fillna(-1)
    df["claim_amount"].fillna(0, inplace=True)
    df["marital_status"].fillna(1, inplace=True)

    # Replace values
    df["marital_status"].replace({1: "Single", 2: "Married"}, inplace=True)
    df["postal_code"].replace({"[\W_]+": ""}, regex=True, inplace=True)

    # Calculate car
    df["car_age"] = calculate_car_age(df["car_registration_year"])
    df["car_age_group"] = pd.cut(x=df["car_age"], bins=4)

    # Customer age
    df["customer_age_group"] = pd.cut(
        df["customer_age"].copy(), bins=np.arange(20, 110, 10), right=False
    )
    df["customer_age_group"].fillna(df["customer_age_group"].min(), inplace=True)

    # Engine power
    df["car_eng_pow_group"] = pd.cut(
        df["car_eng_pow"],
        bins=[0, 100, 250, np.inf],
        labels=["0-100", "100-250", "250+"],
        right=False,
    )

    # Columns to dates
    df["policy_start"] = df["policy_start"].apply(parser.parse)
    df["policy_end"] = df["policy_end"].apply(parser.parse)

    df = calculate_exposure(df, "policy_start", "policy_end")

    df.loc[df["exposure"] > 1, "exposure"] = 1
    df.loc[df["claim_amount"] == 0, "exposure"] = 0


if __name__ == "__main__":
    program()
