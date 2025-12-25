import pandas as pd
import ast


def load_history(csv_path, red_col_index):
    df = pd.read_csv(csv_path)
    df["balls"] = df.iloc[:, red_col_index].apply(
        lambda x: sorted(ast.literal_eval(x)) if pd.notna(x) else []
    )
    return df
