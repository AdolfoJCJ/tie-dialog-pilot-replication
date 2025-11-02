
import yaml, dataclasses
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AnalysisConfig:
    smoothing: dict
    events: dict
    windows: List[int]
    dtw: dict

@dataclass
class Paths:
    ct_series: str
    events: str

@dataclass
class Outputs:
    figures_dir: str
    artifacts_dir: str
    pdf_report: str

@dataclass
class Config:
    seed: int
    data: Paths
    outputs: Outputs
    analysis: AnalysisConfig
    plotting: dict

def load_config(path: str) -> Config:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return Config(
        seed=cfg["seed"],
        data=Paths(**cfg["data"]),
        outputs=Outputs(**cfg["outputs"]),
        analysis=AnalysisConfig(**cfg["analysis"]),
        plotting=cfg.get("plotting", {}),
    )
