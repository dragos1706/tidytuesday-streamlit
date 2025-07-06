import os
import pydytuesday
from pathlib import Path
import pandas as pd

def save_tidy_tuesday_data(date_str: str, base_dir="data"):
    # 1. Make the folder where you want the files
    folder_name = f"week_{date_str}"
    folder_path = os.path.join(base_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # 2. Remember where we started, switch into the new folder
    original_cwd = os.getcwd()
    os.chdir(folder_path)

    try:
        # 3. Download all the files into this folder
        pydytuesday.get_date(date_str)
    finally:
        # 4. Always switch back, even if something fails
        os.chdir(original_cwd)

    return folder_path

def load_tidy_tuesday_data(date_str: str, base_dir: str = "data") -> dict[str, pd.DataFrame]:
    """
    Load all CSVs from data/week_{date_str}/ into pandas DataFrames.

    Parameters
    ----------
    date_str : str
        The TidyTuesday date in YYYY-MM-DD format.
    base_dir : str, optional
        The base data directory (default: "data").

    Returns
    -------
    dict[str, pd.DataFrame]
        A mapping from dataset name (filename without .csv) to its DataFrame.
    """
    folder = Path(base_dir) / f"week_{date_str}"
    if not folder.exists():
        raise FileNotFoundError(f"No data folder found at {folder!r}. Have you run get_date() yet?")

    dataframes: dict[str, pd.DataFrame] = {}
    for csv_file in folder.glob("*.csv"):
        name = csv_file.stem  # e.g. "api_info" from "api_info.csv"
        df = pd.read_csv(csv_file)
        dataframes[name] = df

    return dataframes

if __name__ == "__main__":
    # Example usage
    date_str = "2025-06-10"
    folder_path = save_tidy_tuesday_data(date_str)
    print(f"Tidy Tuesday data saved in: {folder_path}")
    dfs = load_tidy_tuesday_data("2025-06-17")
    print("Loaded datasets:", list(dfs.keys()))
    # globals().update(dfs)
    # You can access the datasets using dfs['dataset_name'] where dataset_name is the name of the dataset without the .csv extension.
    # For example, to access the API categories dataset, use dfs['api_categories'].