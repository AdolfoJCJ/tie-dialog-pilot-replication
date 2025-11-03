#!/usr/bin/env python3
"""
Generate Appendix Figures (B1, B2, B3, B4, B6) for the TIE–Dialog preprint.

Requirements:
- Python 3.9+
- numpy, pandas, matplotlib, scipy

Usage:
    python generate_appendix_figures.py \
        --d2 /path/to/ct_series.2.csv \
        --d4 /path/to/ct_series.4.csv \
        --out ./figures

Notes:
- Figure B6 is a conceptual-but-empirical schematic built from a flattened C_t oscillation with Φ thresholds.
- DTW path (B4) is computed with a basic dynamic-programming implementation to avoid extra dependencies.
"""

import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.spatial.distance import cdist

def ensure_dir(p):
    import os
    os.makedirs(p, exist_ok=True)

def fig_B1(d2_path, out_dir):
    """Figure B1. Illustrative coherence curve (C_t) with annotated rupture and repair events (Dialogue 2)."""
    df = pd.read_csv(d2_path)
    t = df['turn'].values
    ct = df['Ct'].values

    # Peaks (repairs) & valleys (ruptures)
    peaks, _ = find_peaks(ct, prominence=0.03, distance=2)
    valleys, _ = find_peaks(-ct, prominence=0.03, distance=2)

    # Adaptive thresholds
    phi_low = np.percentile(ct, 25)
    phi_high = np.percentile(ct, 75)

    plt.figure(figsize=(9,5))
    plt.plot(t, ct, linewidth=2, label='Coherence trajectory (C_t)')
    if len(peaks):
        plt.scatter(t[peaks], ct[peaks], s=80, label='Repairs (peaks)', zorder=3)
    if len(valleys):
        plt.scatter(t[valleys], ct[valleys], s=80, label='Ruptures (valleys)', zorder=3)

    plt.axhline(phi_low, linestyle='--', linewidth=1.2, label='Φ_low')
    plt.axhline(phi_high, linestyle='--', linewidth=1.2, label='Φ_high')

    plt.xlabel("Turns (t)")
    plt.ylabel("Normalized Coherence (C_t)")
    plt.title("Figure B1. Illustrative coherence curve (C_t) with annotated rupture and repair events")
    plt.grid(alpha=0.3)
    plt.legend(frameon=True, loc='lower right')
    plt.tight_layout()
    plt.savefig(f"{out_dir}/Figure_B1_Ct_rupture_repair.png", dpi=300)
    plt.close()

def fig_B2(d2_path, out_dir):
    """Figure B2. Dialogue 2 — High structural alignment (r_warped = 0.98, dist_norm = 0.98)."""
    df = pd.read_csv(d2_path)
    t = df['turn'].values
    ct_model = df['Ct'].values
    ct_human = df['Ct_Im'].values

    plt.figure(figsize=(9,5))
    plt.plot(t, ct_human, linewidth=2, label='Human (Ct_Im, field alignment)')
    plt.plot(t, ct_model, linewidth=2, label='Model (Ct local, smoothed)')
    plt.xlabel("Turns (t)")
    plt.ylabel("Normalized Coherence (C_t)")
    plt.title("Figure B2. Dialogue 2 — High structural alignment (r_warped = 0.98, dist_norm = 0.98)")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(frameon=True, loc='lower right')
    plt.tight_layout()
    plt.savefig(f"{out_dir}/Figure_B2_Dialogue2_alignment.png", dpi=300)
    plt.close()

def fig_B3(d4_path, out_dir):
    """Figure B3. Dialogue 4 — Phase inversion and proto-coherence (r_warped = 0.98, lag ≈ -1.23)."""
    df = pd.read_csv(d4_path)
    t = df['turn'].values
    ct_model = df['Ct'].values
    ct_human = df['Ct_Im'].values

    plt.figure(figsize=(9,5))
    plt.plot(t, ct_human, linewidth=2, label='Human (Ct_Im, field alignment)')
    plt.plot(t, ct_model, linewidth=2, label='Model (Ct local, smoothed)')
    plt.xlabel("Turns (t)")
    plt.ylabel("Normalized Coherence (C_t)")
    plt.title("Figure B3. Dialogue 4 — Phase inversion and proto-coherence (r_warped = 0.98, lag ≈ -1.23)")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(frameon=True, loc='lower right')
    plt.tight_layout()
    plt.savefig(f"{out_dir}/Figure_B3_Dialogue4_proto_coherence.png", dpi=300)
    plt.close()

def dtw_path_matrix(x, y):
    """Compute DTW accumulated cost and backtracked path (i,j)."""
    D = cdist(x.reshape(-1,1), y.reshape(-1,1), metric='euclidean')
    n, m = D.shape
    acc = np.zeros((n, m))
    acc[0, 0] = D[0, 0]
    for i in range(1, n):
        acc[i, 0] = D[i, 0] + acc[i-1, 0]
    for j in range(1, m):
        acc[0, j] = D[0, j] + acc[0, j-1]
    for i in range(1, n):
        for j in range(1, m):
            acc[i, j] = D[i, j] + min(acc[i-1, j], acc[i, j-1], acc[i-1, j-1])

    i, j = n-1, m-1
    path = [(i, j)]
    while i > 0 and j > 0:
        step = np.argmin([acc[i-1, j-1], acc[i-1, j], acc[i, j-1]])
        if step == 0:
            i, j = i-1, j-1
        elif step == 1:
            i, j = i-1, j
        else:
            j = j-1
        path.append((i, j))
    path.reverse()
    return D, path

def fig_B4(d2_path, out_dir):
    """Figure B4. DTW warping path for Dialogue 2 (human ↔ model)."""
    df = pd.read_csv(d2_path)
    human = df['Ct_Im'].values
    model = df['Ct'].values

    D, path = dtw_path_matrix(human, model)
    path_y, path_x = zip(*path)

    plt.figure(figsize=(6,6))
    plt.imshow(D, cmap='cividis', origin='lower', aspect='auto')
    plt.plot(path_x, path_y, color='white', linewidth=2, label='Optimal path')
    plt.xlabel("Model time steps")
    plt.ylabel("Human time steps")
    plt.title("Figure B4. DTW warping path for Dialogue 2 (human ↔ model)")
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(f"{out_dir}/Figure_B4_DTW_Dialogue2.png", dpi=300)
    plt.close()

def fig_B6(out_dir):
    """Figure B6. The Informational Heartbeat — S–B–R Cycle with Φ Thresholds (Flattened C_t)."""
    t = np.linspace(0, 6*np.pi, 120)
    ct = 0.65 + 0.04*np.sin(t)  # flattened oscillation
    phi_low, phi_high = 0.60, 0.75

    plt.figure(figsize=(9,4))
    plt.plot(t, ct, linewidth=2.5, label='Coherence trajectory (C_t)')
    plt.axhline(phi_low, linestyle='--', linewidth=1.2, label='Φ_low')
    plt.axhline(phi_high, linestyle='--', linewidth=1.2, label='Φ_high')
    plt.text(1.0, 0.73, 'S (Stability)', fontsize=11)
    plt.text(3.2, 0.58, 'B (Breakdown)', fontsize=11)
    plt.text(5.6, 0.72, 'R (Repair)', fontsize=11)
    plt.xlabel("Turns (t)")
    plt.ylabel("Normalized Coherence (C_t)")
    plt.title("Figure B6. The Informational Heartbeat — S–B–R Cycle with Φ Thresholds (Flattened C_t)")
    plt.ylim(0.55, 0.78)
    plt.grid(alpha=0.3)
    plt.legend(frameon=True, loc='upper right')
    plt.tight_layout()
    plt.savefig(f"{out_dir}/Figure_B6_Informational_Heartbeat.png", dpi=300)
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--d2", required=True, help="Path to ct_series.2.csv (Dialogue 2)")
    ap.add_argument("--d4", required=True, help="Path to ct_series.4.csv (Dialogue 4)")
    ap.add_argument("--out", default="./figures", help="Output directory for figures")
    args = ap.parse_args()

    ensure_dir(args.out)

    fig_B1(args.d2, args.out)
    fig_B2(args.d2, args.out)
    fig_B3(args.d4, args.out)
    fig_B4(args.d2, args.out)
    fig_B6(args.out)

    print("Saved figures to:", args.out)

if __name__ == "__main__":
    main()
