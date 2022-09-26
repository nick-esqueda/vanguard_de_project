import pandas as pd


def write_to_csv(data, filepath):
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    print(f"Done writing data to {filepath}")