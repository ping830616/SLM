#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from exact.fig5 import plot_benign_sparse_causal_network_two_panel


def main() -> None:
    p = argparse.ArgumentParser(description="Plot the benign sparse causal network (Fig. 5 style).")
    p.add_argument("--edges-a", type=Path, required=True, help="CSV with columns u,v,strength,(optional)domain_u,domain_v for Setup A.")
    p.add_argument("--edges-b", type=Path, required=True, help="CSV with columns u,v,strength,(optional)domain_u,domain_v for Setup B.")
    p.add_argument("--out", type=Path, default=Path("./results/figures/fig5_benign_sparse_causal_network.png"))
    p.add_argument("--title-a", type=str, default="Setup A")
    p.add_argument("--title-b", type=str, default="Setup B")
    args = p.parse_args()

    plot_benign_sparse_causal_network_two_panel(
        edges_csv_A=args.edges_a,
        edges_csv_B=args.edges_b,
        out_png=args.out,
        title_A=args.title_a,
        title_B=args.title_b,
    )


if __name__ == "__main__":
    main()
