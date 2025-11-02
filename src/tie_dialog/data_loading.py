
import pandas as pd

def load_ct_series(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    needed = {"dialogue_id","turn","human_ct","model_ct"}
    if not needed.issubset(df.columns):
        raise ValueError(f"ct_series missing columns: {needed - set(df.columns)}")
    return df.sort_values(["dialogue_id","turn"])

def load_events(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    needed = {"dialogue_id","turn","human_peak","human_valley","machine_peak","machine_valley"}
    if not needed.issubset(df.columns):
        raise ValueError(f"events missing columns: {needed - set(df.columns)}")
    return df.sort_values(["dialogue_id","turn"])
