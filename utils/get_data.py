import os
import pandas as pd


def combine_files(file_list: list) -> pd.DataFrame:
    """Appends csv files one on top of the other.

    Args:
        file_list (list): file name list in a particular folder.

    Returns:
        pd.DataFrame: a new DataFrame consisting of the rows of all csv files in the file_list.
    """

    csv_list = []
    [
        csv_list.append(pd.read_csv(file).assign(file_Name=os.path.basename(file)))
        for file in sorted(file_list)
    ]

    csv_merged = pd.concat(csv_list, ignore_index=True)

    return csv_merged


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

