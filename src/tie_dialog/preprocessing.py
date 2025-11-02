
import pandas as pd

def smooth_series(df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    out = df.copy()
    if window and window > 1:
        out["human_ct"] = out.groupby("dialogue_id")["human_ct"].transform(lambda s: s.rolling(window, min_periods=1).mean())
        out["model_ct"] = out.groupby("dialogue_id")["model_ct"].transform(lambda s: s.rolling(window, min_periods=1).mean())
    return out
