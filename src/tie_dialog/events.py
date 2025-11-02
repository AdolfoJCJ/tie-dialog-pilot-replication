
import pandas as pd
import numpy as np
from scipy.signal import find_peaks

def detect_events(ct_df: pd.DataFrame, prominence=0.08, min_distance=2):
    rows = []
    for did, part in ct_df.groupby("dialogue_id"):
        # Peaks for human & model
        for who in ["human_ct","model_ct"]:
            y = part[who].values
            peaks, _ = find_peaks(y, prominence=prominence, distance=min_distance)
            valleys, _ = find_peaks(-y, prominence=prominence, distance=min_distance)
            for p in peaks:
                rows.append({"dialogue_id": did, "turn": int(part.iloc[p]["turn"]), f"{who.split('_')[0]}_peak": 1, f"{who.split('_')[0]}_valley": 0})
            for v in valleys:
                rows.append({"dialogue_id": did, "turn": int(part.iloc[v]["turn"]), f"{who.split('_')[0]}_peak": 0, f"{who.split('_')[0]}_valley": 1})
    ev = pd.DataFrame(rows).fillna(0)
    # pivot to single row per (dialogue_id, turn)
    if ev.empty:
        return ct_df[["dialogue_id","turn"]].assign(human_peak=0,human_valley=0,machine_peak=0,machine_valley=0)
    ev = ev.groupby(["dialogue_id","turn"]).sum(numeric_only=True).reset_index()
    # Ensure all cols
    for c in ["human_peak","human_valley","machine_peak","machine_valley"]:
        if c not in ev.columns: ev[c]=0
    return ev[["dialogue_id","turn","human_peak","human_valley","machine_peak","machine_valley"]]

def match_events(ev_h, ev_m, window):
    # Return matches within ±window turns
    matches = 0
    total = 0
    for kind in ["peak","valley"]:
        a = set(tuple(x) for x in ev_h.query(f"human_{kind}==1")[["dialogue_id","turn"]].to_numpy())
        b = set(tuple(x) for x in ev_m.query(f"machine_{kind}==1")[["dialogue_id","turn"]].to_numpy())
        total += len(a)
        if window == 0:
            matches += len(a & b)
        else:
            # expand a by window and check membership
            for (d,t) in a:
                ok = any((d, t+shift) in b for shift in range(-window, window+1))
                matches += 1 if ok else 0
    precision = matches / (len(b) if len(b)>0 else 1)
    recall = matches / (total if total>0 else 1)
    f1 = 0 if (precision+recall)==0 else 2*precision*recall/(precision+recall)
    return dict(window=window, precision=precision, recall=recall, f1=f1)
