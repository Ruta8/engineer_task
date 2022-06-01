import os
import pandas as pd


def concat_files(file_list: list) -> pd.DataFrame:
    """Appends csv files one on top of the other.

    Args:
        file_list (list): file name list in a particular folder.

    Returns:
        pd.DataFrame: a new DataFrame consisting of the rows of all csv files in the file_list.
    """
    csv_list = []
    [
        csv_list.append(
            pd.DataFrame(pd.read_csv(file).assign(file_Name=os.path.basename(file)))
        )
        for file in file_list
    ]

    merged_csv = pd.concat(csv_list)

    return merged_csv


def get_file_list(data_path: str, file_names_start_with: str = None) -> list:
    """Creates a list of files in a folder.

    Args:
        data_path (str): folder where all the files are
        starts_with (str, optional): if there are other files in the folder, specify how the names of the files start.

    Returns:
        list: list: a list of file names in a specified folder.
    """
    file_list = [
        data_path + file_name
        if file_name.startswith(f"{file_names_start_with}")
        else data_path + file_name
        for file_name in os.listdir(data_path)
    ]

    return file_list


def combine_files():

    raw_folder_file_list = get_file_list(
        data_path="data/raw/", file_names_start_with="task_data"
    )
    concatanated_files = concat_files(raw_folder_file_list)

    df = concatanated_files.merge(
        pd.read_csv("data/external/POLICY_DATA.csv"), how="left", on="policy_id"
    )

    return df
