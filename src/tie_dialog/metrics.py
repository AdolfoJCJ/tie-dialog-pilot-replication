
import pandas as pd
from sklearn.metrics import cohen_kappa_score

def binary_series(df, col_name):
    # Expand to full index of (dialogue_id, turn)
    idx = df[["dialogue_id","turn"]].drop_duplicates().sort_values(["dialogue_id","turn"])
    y = df.set_index(["dialogue_id","turn"])[col_name].reindex(pd.MultiIndex.from_frame(idx)).fillna(0).astype(int)
    return y.values

def cohen_kappa(ev_ref: pd.DataFrame, ev_sys: pd.DataFrame, kind="peak"):
    # compares human_kind vs machine_kind
    ref_col = f"human_{kind}"
    sys_col = f"machine_{kind}"
    df = ev_ref.merge(ev_sys, on=["dialogue_id","turn"], how="outer").fillna(0)
    y_true = df[ref_col].astype(int)
    y_pred = df[sys_col].astype(int)
    return cohen_kappa_score(y_true, y_pred)

def macro_average(rows, key="f1"):
    return sum(r[key] for r in rows)/len(rows) if rows else 0.0
