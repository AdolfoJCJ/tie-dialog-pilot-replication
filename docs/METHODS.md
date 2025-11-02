
# METHODS (Pilot Replication)

- **Coherence curves (𝒞ₜ)**: Loaded from `ct_series.*.csv` or computed from embeddings; smoothed via rolling mean.  
- **Event detection**: Peaks/valleys via prominence/width thresholds; windows ±1..±3 for matching human vs. machine events.  
- **Agreement metrics**: Precision/Recall/F1 per event type and window size; Cohen’s κ (pairwise) and Fleiss/Light κ (multi-rater).  
- **DTW**: `dtaidistance` to obtain warped correlation (r_warped), normalized distance and lag; directionality estimated via cross-correlation of aligned paths.  
- **Reporting**: Figures (overlays, event rasters, DTW path), tables (per-dialogue & macro averages), and optional PDF assembly.
