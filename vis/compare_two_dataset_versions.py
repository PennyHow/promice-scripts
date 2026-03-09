#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

if __name__ == '__main__':

    stations = ["CEN", "CP1", "DY2", "EGP", "FRE", "HUM", "JAR",
               "KAN_B", "KAN_L", "KAN_M", "KAN_T", "KAN_U",
               "KPC_L", "KPC_U", "LYN_L", "LYN_T", "MIT",
               "NAE", "NAU", "NEM", "NSE", "NUK_K",
               "NUK_L", "QAS_A", "QAS_L",
               "QAS_M", "QAS_U", "RED_L",
               "SCO_L", "SCO_U", "SDL", "SDM", "SER_B", "SWC",
               "TAS_A", "TAS_L", "THU_L", "THU_L2", "THU_U", "TUN",
               "UPE_L", "UPE_U", "WEG_B", "WEG_L",
               "ZAC_A", "ZAC_L", "ZAC_U"]

    variables = ["t_u", "t_l",
                 "p_u", "p_l",
                 "rh_u", "rh_l",
                 "wspd_u", "wspd_l",
                 "t_i_1", "t_i_2", "t_i_3", "t_i_4",
                 "t_i_5", "t_i_6", "t_i_7", "t_i_8",
                 "t_i_9", "t_i_10"]

    output_pdf = "ROC_filter_comparison.pdf"

    with PdfPages(output_pdf) as pdf:

        for station in stations:

            infile1 = "https://thredds.geus.dk/thredds/dodsC/aws/l3sites/netcdf/hour/" + station + "_hour.nc"
            ds1 = xr.open_dataset(infile1)

            infile2 = "/home/pho/Downloads/sites-promice-03/" + station + "/" + station + "_hour.nc"
            ds2 = xr.open_dataset(infile2)

            ds1_aligned, ds2_aligned = xr.align(ds1, ds2, join="inner")

            for variable in variables:
                if not variable in ds1_aligned: continue

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

                    plt.plot(v1.time, v1, label="geus-promice-02", alpha=0.5)
                    plt.plot(v2.time, v2, label="geus-promice-03", alpha=0.8)

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

                    pdf.savefig(fig)
                    plt.close(fig)

    print(f"\nSaved output to {output_pdf}")