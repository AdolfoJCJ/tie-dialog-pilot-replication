
import argparse, os, json, random, numpy as np, pandas as pd
from tie_dialog.config import load_config
from tie_dialog.logging_setup import setup_logger
from tie_dialog.data_loading import load_ct_series, load_events
from tie_dialog.preprocessing import smooth_series
from tie_dialog.events import detect_events, match_events
from tie_dialog.metrics import cohen_kappa, macro_average
from tie_dialog.dtw_analysis import per_dialogue
from tie_dialog.plots import plot_overlay

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--stage", choices=["metrics","figures","report","all"], default="all")
    args = ap.parse_args()

    log = setup_logger()
    cfg = load_config(args.config)
    random.seed(cfg.seed); np.random.seed(cfg.seed)

    os.makedirs(cfg.outputs.figures_dir, exist_ok=True)
    os.makedirs(cfg.outputs.artifacts_dir, exist_ok=True)

    ct = load_ct_series(cfg.data.ct_series)
    ct = smooth_series(ct, window=cfg.analysis["smoothing"]["window"] if isinstance(cfg.analysis, dict) else cfg.analysis.smoothing["window"])

    # Events: use provided annotations if available; otherwise detect from C_t
    if os.path.exists(cfg.data.events):
        ev = load_events(cfg.data.events)
    else:
        log.info("No events CSV found; detecting events from C_t.")
        ev = detect_events(ct, prominence=cfg.analysis["events"]["peak_prominence"], min_distance=cfg.analysis["events"]["min_distance"])

    # === METRICS ===
    if args.stage in ("metrics","all"):
        rows = []
        for w in cfg.analysis["windows"] if isinstance(cfg.analysis, dict) else cfg.analysis.windows:
            # Build per-dialogue event frames
            per_d = []
            for did, part in ev.groupby("dialogue_id"):
                # split human vs machine into separate views for matching
                per_d.append(match_events(part, part, w))  # placeholder self-match; replace with human vs machine if separate
            # compute macro averages over all dialogues (here replicated via ev)
            res = match_events(ev, ev, w)  # self-match demo
            rows.append(res)

        df_f1 = pd.DataFrame(rows)
        f1_macro = df_f1["f1"].mean()
        df_f1.to_csv(os.path.join(cfg.outputs.artifacts_dir, "f1_by_window.csv"), index=False)
        log.info(f"Saved F1 by window -> artifacts/f1_by_window.csv (macro={f1_macro:.3f})")

        # DTW per-dialogue
        df_dtw = per_dialogue(ct)
        df_dtw.to_csv(os.path.join(cfg.outputs.artifacts_dir, "dtw_summary.csv"), index=False)
        log.info("Saved dtw_summary.csv")

    # === FIGURES ===
    fig_paths = []
    if args.stage in ("figures","all"):
        for did in ct["dialogue_id"].unique():
            p = plot_overlay(ct, cfg.outputs.figures_dir, did, figsize=tuple(cfg.plotting.get("figsize",[10,4])), dpi=cfg.plotting.get("dpi",160), font_size=cfg.plotting.get("font_size",11))
            if p: fig_paths.append(p)

    # === REPORT ===
    if args.stage in ("report","all"):
        try:
            from tie_dialog.report import build_pdf
            tables = {
                "F1 by window": os.path.join(cfg.outputs.artifacts_dir, "f1_by_window.csv"),
                "DTW summary": os.path.join(cfg.outputs.artifacts_dir, "dtw_summary.csv"),
            }
            out_pdf = cfg.outputs.pdf_report
            build_pdf(fig_paths, tables, out_pdf)
        except Exception as e:
            log.warning(f"PDF generation skipped: {e}")

if __name__ == "__main__":
    main()
