
import os
import matplotlib.pyplot as plt
import pandas as pd

def plot_overlay(df, outdir, did, figsize=(10,4), dpi=160, font_size=11):
    part = df[df["dialogue_id"]==did]
    if part.empty: return None
    plt.figure(figsize=figsize, dpi=dpi)
    plt.plot(part["turn"], part["human_ct"], label="Human")
    plt.plot(part["turn"], part["model_ct"], label="Model")
    plt.xlabel("Turn")
    plt.ylabel("Coherence (C_t)")
    plt.title(f"Dialogue {did} — Human vs Model C_t")
    plt.legend()
    path = os.path.join(outdir, f"ct_overlay_d{did}.png")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
