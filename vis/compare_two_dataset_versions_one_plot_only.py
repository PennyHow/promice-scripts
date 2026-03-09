#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

if __name__ == '__main__':

    station = "QAS_L"

    variable = "wspd_u"


    infile1 = "https://thredds.geus.dk/thredds/dodsC/aws/l3sites/netcdf/hour/" + station + "_hour.nc"
    ds1 = xr.open_dataset(infile1)

    infile2 = "/home/pho/Desktop/sites_with_ROC_filter/" + station + "/" + station + "_hour.nc"
    ds2 = xr.open_dataset(infile2)

    ds1_aligned, ds2_aligned = xr.align(ds1, ds2, join="inner")

    v1 = ds1_aligned[variable]
    v2 = ds2_aligned[variable]

    removed_mask = v1.notnull() & v2.isnull()

    n_removed = removed_mask.sum().item()
    n_total = v1.notnull().sum().item()
    percent_removed = 100 * n_removed / n_total if n_total > 0 else 0

    print(f"{station} {variable}: Removed {n_removed} points "
          f"({percent_removed:.2f}% of valid data)")

    if n_total > 0:
        # --------------------
        # 1️⃣ Plot page
        # --------------------
        fig = plt.figure(figsize=(12, 5))

        plt.plot(v1.time, v1, label="Original", alpha=0.5)
        plt.plot(v2.time, v2, label="Filtered", alpha=0.8)

        plt.scatter(
            v1.time.where(removed_mask),
            v1.where(removed_mask),
            color="red",
            s=12,
            label="Removed values"
        )

        plt.legend(loc=4)
        plt.title(f"{station} – {variable} - Removed points: {n_removed}")

        plt.tight_layout()

        plt.show()