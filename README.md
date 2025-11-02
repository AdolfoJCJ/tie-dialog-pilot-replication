
# TIE–Dialog Pilot Replication

**Goal:** Provide a clean, one-command pipeline to reproduce the key results of the *Human–Machine Coherence* pilot:
- Coherence curves (𝒞ₜ) for human vs. model
- Event detection (peaks/valleys) with ±1…±3 windows
- DTW alignment metrics (`r_warped`, normalized distance, lag)
- Agreement metrics (F1, Cohen’s κ, Fleiss/Light κ)
- Figures and an auto-generated PDF report

> Last updated: 2025-11-02

---

## 1) Quickstart

```bash
# Option A — Conda
conda env create -f environment.yml
conda activate tie-dialog-pilot

# Option B — Pip
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# Run the full pipeline with the sample data
make all
# or
python scripts/run_pipeline.py --config configs/config.sample.yml
```

Artifacts will be saved under `reports/` and `reports/figures/`.

---

## 2) Repository layout

```
.
├── CITATION.cff
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
├── environment.yml
├── configs/
│   ├── config.sample.yml
│   └── thresholds.example.yml
├── data/
│   ├── README.md
│   ├── external/        # third-party raw data (not versioned)
│   ├── interim/         # intermediate data
│   ├── processed/       # final processed datasets
│   └── raw/             # original CSVs (humans & model)
├── docs/
│   ├── HOWTO.md
│   └── METHODS.md
├── scripts/
│   └── run_pipeline.py
├── src/
│   ├── tie_dialog/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging_setup.py
│   │   ├── data_loading.py
│   │   ├── preprocessing.py
│   │   ├── coherence.py
│   │   ├── events.py
│   │   ├── metrics.py
│   │   ├── dtw_analysis.py
│   │   ├── plots.py
│   │   └── report.py
│   └── tests/
│       ├── test_metrics.py
│       └── test_events.py
└── reports/
    ├── figures/
    ├── artifacts/
    └── README.md
```

---

## 3) Data expected

Place your CSVs in `data/raw/`. Minimum expected files:

- `ct_series.sample.csv` — time series with columns:
  - `dialogue_id`, `turn`, `human_ct`, `model_ct`  (𝒞ₜ values)
- `events_template.sample.csv` — event annotations:
  - `dialogue_id`, `turn`, `human_peak`, `human_valley`, `machine_peak`, `machine_valley` (0/1 flags)

> You can replace the sample files with the actual data, keeping headers.

---

## 4) Configuration

Edit `configs/config.sample.yml` (or copy to `configs/config.yml`) to change windows, thresholds and files.

Key params:
- `windows: [1,2,3]` — evaluation windows ±k
- `peak_prominence`, `valley_prominence` — detection parameters
- `smoothing` — rolling window etc.
- paths under `data:` and `reports:`

---

## 5) Reproducible pipeline

- Deterministic seeds & versions logged
- All params stored in YAML and exported with artifacts
- One command (`make all`) regenerates figures & report

---

## 6) Citing

See `CITATION.cff`. 

---

## 7) License

MIT (see `LICENSE`)
