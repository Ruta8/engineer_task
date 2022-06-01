import datetime
import logging
import numpy as np
import pandas as pd
import dateutil.parser as parser


def fillna_with_mode(df, column_list):

    [df.fillna(df[column].mode(), inplace=True) for column in column_list]

    logging.info(f"Missing values in column list {column_list} where filled with the column mode.")

    return df

def fillna_with_int(df, column_list, int):

    df[column_list] = df[column_list].fillna(int)

    return df

def replace_values(df, column_list, value_dictionary):

    df[column_list] = df[column_list].replace(value_dictionary, regex=True)

    logging.info(f"Missing values in column list {column_list} where filled with value_dictionary respectively.")

    return df

def parse_dates(df, column_list):
    
    for column in column_list:
        df[column] = df[column].apply(parser.parse)

    logging.info(f"Columns in column list {column_list} where parsed as dates.")

    return df

def group_column(df, column, bins, labels:list=None):
    
    df[f'{column}_group'] = pd.cut(x=df[f'{column}'], bins=bins, right=False, labels=labels)

    logging.info(f"New column {column}_group was created.")

    return df

def transform(df):

    df = fillna_with_mode(df, ["car_brand", "postal_code"])
    df = fillna_with_int(df,["car_eng_pow", "customer_age"], -1)
    df = fillna_with_int(df,["claim_amount"], 0)
    df = fillna_with_int(df,["marital_status"], 1)

    df = replace_values(df,["marital_status"],{1: "Single", 2: "Married"})
    # regex below removes whitespace and ‘-’ symbol
    df = replace_values(df,["postal_code"], {"[\W_]+": ""})
    
    df["car_age"] = datetime.datetime.now() - pd.to_datetime(df['car_registration_year'], format="%Y")
    df["car_age"] = (df["car_age"] / np.timedelta64(1, "Y")).astype("float").round(1)

    df = group_column(df, "car_age", 4)
    df = group_column(df, "car_eng_pow", bins=[0, 100, 250, np.inf], labels=["0-100", "100-250", "250+"])
    df = group_column(df, "customer_age", np.arange(20, 110, 10))

    df["customer_age_group"] = df["customer_age_group"].fillna(df["customer_age_group"].min())

    df = parse_dates(df, ["policy_start", "policy_end"])

    df["exposure"] = (df["policy_end"] - df["policy_start"]) / np.timedelta64(1, "Y")
    df["exposure"] = df["exposure"].astype("float")
    df.loc[df["exposure"] > 1, "exposure"] = 1
    df.loc[df["claim_amount"] == 0, "exposure"] = 0

    return df
