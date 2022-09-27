import pandas as pd


def write_to_csv(data, filepath):
    if type(data) is not pd.DataFrame:
        data = pd.DataFrame(data)
    data.to_csv(filepath, index=False)
    print(f"Done writing data to {filepath}")