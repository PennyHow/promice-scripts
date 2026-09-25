#!/usr/bin/env python3
import os, sys
from pathlib import Path

import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

indir = Path("/home/pho/aws-env/aws-ops/aws-l2/level_2")
output_pdf = "heading_comparison.pdf"

with PdfPages(output_pdf) as pdf:

    for station in sorted(indir.glob("**/*_hour.nc")):

        station_name = str(station.stem).split("_hour")[0]

        thredds_path = (
            "https://thredds.geus.dk/thredds/dodsC/aws/l2stations/netcdf/hour/"
            + station_name + "_hour.nc"
        )

        try:
            ds1 = xr.open_dataset(thredds_path)
        except:
            continue

        ds2 = xr.open_dataset(station)

        ds1_aligned, ds2_aligned = xr.align(ds1, ds2, join="inner")

        compare = [
            ["rot", "rot_magnetic"],
            ["rot", "rot_true"]
        ]

        for variable in compare:

            if variable[0] not in ds1_aligned:
                continue
            if variable[1] not in ds2_aligned:
                continue

            v1 = ds1_aligned[variable[0]]
            v2 = ds2_aligned[variable[1]]

            removed_mask = v1.notnull() & v2.isnull()
            valid_mask = v1.notnull() & v2.notnull()

            n_removed = removed_mask.sum().item()
            n_total = v1.notnull().sum().item()
            percent_removed = 100 * n_removed / n_total if n_total > 0 else 0

            diff = (v2 - v1).where(valid_mask)
            percent_diff = 100 * diff / abs(v1).clip(min=1e-6)

            mean_abs_change = abs(diff).mean().item()
            median_abs_change = abs(diff).median().item()
            mean_change = diff.mean().item()
            rmse = ((diff ** 2).mean() ** 0.5).item()

            mean_percent_change = percent_diff.mean().item()
            median_percent_change = percent_diff.median().item()
            max_abs_change = abs(diff).max().item()

            correlation = xr.corr(
                v1.where(valid_mask),
                v2.where(valid_mask)
            ).item()

            # ---------------------------------
            # Stats string for figure
            # ---------------------------------
            stats_text = (
                f"{station_name} | {variable[0]} vs {variable[1]}\n"
                f"Removed: {n_removed} points ({percent_removed:.2f}%)\n"
                f"Mean change: {mean_change:.4f}\n"
                f"Mean abs change: {mean_abs_change:.4f}\n"
                f"Median abs change: {median_abs_change:.4f}\n"
                f"RMSE: {rmse:.4f}\n"
                f"Mean % change: {mean_percent_change:.2f}%\n"
                f"Median % change: {median_percent_change:.2f}%\n"
                f"Max abs change: {max_abs_change:.4f}\n"
                f"Correlation: {correlation:.4f}\n"
                )

            print(stats_text)
            print("-" * 60)

          #  if mean_percent_change >= 1.:

            # ---------------------------------
            # Figure with subplots
            # ---------------------------------
            fig, (ax1, ax2) = plt.subplots(
                2, 1,
                figsize=(14, 8),
                sharex=True,
                gridspec_kw={"height_ratios": [2, 1]}
            )

            # --------------------
            # Top: comparison
            # --------------------
            ax1.plot(v1.time, v1, label="THREDDS (v1.11.3)", alpha=0.5)
            ax1.plot(v2.time, v2, label="DEV (v1.12.0)", alpha=0.8)

            ax1.set_title(f"{station_name} – {variable[0]} vs {variable[1]}")
            ax1.legend(loc="upper right")

            # Put stats inside top plot
            ax1.text(
                0.01, 0.99,
                stats_text,
                transform=ax1.transAxes,
                fontsize=9,
                verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
            )

            # --------------------
            # Bottom: difference
            # --------------------
            ax2.plot(diff.time, diff, color="black", alpha=0.6)
            ax2.axhline(0, color="red", linewidth=1, alpha=0.5)

            ax2.set_title("Difference (v2 - v1)")
            ax2.set_ylabel("Diff")

            plt.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

print(f"\nSaved output to {output_pdf}")