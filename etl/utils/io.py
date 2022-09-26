import pandas as pd


def send_to_csv(data, filepath):
    df = pd.DataFrame(data)
    df.to_csv(filepath)
    print(f"Done writing data to {filepath}")