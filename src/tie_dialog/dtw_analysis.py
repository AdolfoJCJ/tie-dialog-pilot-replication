
import numpy as np
import pandas as pd
from dtaidistance import dtw

def dtw_pair(h, m):
    d = dtw.distance(h, m)
    # naive warped correlation proxy (for demo purposes)
    r = np.corrcoef(h, m)[0,1]
    return d, r

def per_dialogue(df: pd.DataFrame):
    rows = []
    for did, part in df.groupby("dialogue_id"):
        h = part["human_ct"].values
        m = part["model_ct"].values
        d, r = dtw_pair(h, m)
        rows.append(dict(dialogue_id=did, dist_norm=float(d), r_warped=float(r)))
    return pd.DataFrame(rows)
