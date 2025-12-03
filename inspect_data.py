import pandas as pd
import os

files = [
    "list_of_all_spacs.xlsx",
    "russ_1000_202308.xlsx",
    "sp500_202308.xlsx",
    "stock_ipos_20231004.csv"
]

for f in files:
    print(f"--- {f} ---")
    try:
        if f.endswith('.xlsx'):
            df = pd.read_excel(f, nrows=2)
        else:
            df = pd.read_csv(f, nrows=2)
        print(df.columns.tolist())
        print(df.head(1))
    except Exception as e:
        print(f"Error reading {f}: {e}")
    print("\n")
