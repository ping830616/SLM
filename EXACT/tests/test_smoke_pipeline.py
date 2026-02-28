from __future__ import annotations

from pathlib import Path

from exact.experiments.ets2026 import ETS2026Config, run_ets2026


def test_sample_pipeline_runs(tmp_path: Path) -> None:
    data_root = Path(__file__).resolve().parents[1] / "data" / "sample"
    out_root = tmp_path / "out"

    cfg = ETS2026Config(
        window_sizes=(50, 100, 200),
        n_splits=3,
        lambda_res=0.5,
        agg_mode="max",
    )

    artifacts = run_ets2026(data_root=data_root, out_root=out_root, cfg=cfg)

    # basic sanity checks
    assert "shared_features" in artifacts
    assert len(artifacts["shared_features"]) > 0

    # summaries should exist
    assert (out_root / "SETUP_A_EXACT_summary_per_workload.csv").exists()
    assert (out_root / "SETUP_B_EXACT_summary_per_workload.csv").exists()

    # plot should exist
    assert (out_root / "figures" / "fig4_metrics_vs_window_size.png").exists()
