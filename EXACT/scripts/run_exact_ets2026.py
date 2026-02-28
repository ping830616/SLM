#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from exact.experiments.ets2026 import ETS2026Config, run_ets2026


def main() -> None:
    p = argparse.ArgumentParser(description="Run the notebook-derived EXACT pipeline (ETS 2026 draft).")
    p.add_argument("--data-root", type=Path, required=True, help="Folder containing telemetry CSVs (DDR4_*.csv and DDR5_*.csv).")
    p.add_argument("--out-root", type=Path, default=Path("./results"), help="Output folder for CSVs and figures.")
    p.add_argument("--lambda-res", type=float, default=0.5, help="λ mixing coefficient in CINTAS score.")
    p.add_argument("--agg-mode", type=str, default="max", choices=["max", "mean", "median"], help="Decision-block aggregation mode.")
    p.add_argument("--p-quantile", type=float, default=0.99, help="Benign quantile for threshold τ.")
    p.add_argument("--corr-threshold", type=float, default=0.35, help="Spearman |rho| threshold for benign correlation skeleton.")
    args = p.parse_args()

    cfg = ETS2026Config(
        lambda_res=float(args.lambda_res),
        agg_mode=str(args.agg_mode),
        p_quantile=float(args.p_quantile),
        corr_threshold=float(args.corr_threshold),
    )

    run_ets2026(data_root=args.data_root, out_root=args.out_root, cfg=cfg)


if __name__ == "__main__":
    main()
