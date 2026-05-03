import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pygris

pd.set_option("mode.copy_on_write", True)

import os

os.makedirs("30_results/figures", exist_ok=True)

import warnings

warnings.filterwarnings("ignore")

mental_health_df = pd.read_csv("20_intermediate_files/clean_mh_dataset.csv")

nc_counties = pygris.counties(state="NC", cb=True, year=2023)

nc_counties["GEOID"] = nc_counties["GEOID"].astype("int64")

mental_health_gdf = nc_counties.merge(
    mental_health_df, left_on="GEOID", right_on="fips", how="inner"
)

threshold = mental_health_gdf["providers_per_100k"].median()  # could be changed later

high_access = mental_health_gdf[mental_health_gdf["providers_per_100k"] >= threshold]

low_access = mental_health_gdf[mental_health_gdf["providers_per_100k"] < threshold]


# figure 1: distribution of high and low access with observed distress
fig1, (ax11, ax12) = plt.subplots(1, 2)

high_access["observed_distress"].hist(ax=ax11)
ax11.set_title("High Access")
low_access["observed_distress"].hist(ax=ax12)
ax12.set_title("Low Access")

fig1.savefig(
    "30_results/figures/figA7_distress_distribution_high_vs_low.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig1)


"""
mental_health_df.groupby(mental_health_df["providers_per_100k"] >= threshold)[
    ["observed_distress", "loneliness_rate", "unemployment_rate"]
].mean()
"""

fig2, (ax21, ax22) = plt.subplots(1, 2)

mental_health_gdf.plot(column="providers_per_100k", legend=True, ax=ax21)
ax21.set_title("Mental Health Care Providers per 100k people in NC Counties")
mental_health_gdf.plot(column="observed_distress", legend=True, ax=ax22)
ax21.set_title("Frequent Mental Health Distress in NC Counties")

fig2.savefig(
    "30_results/figures/fig1_provider_access_map.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig2)

# create column for high access
mental_health_gdf["high_access"] = mental_health_gdf["providers_per_100k"] >= threshold

mental_health_gdf["low_access"] = mental_health_gdf["providers_per_100k"] < threshold

# figure 3: low access counties
fig3, ax31 = plt.subplots()

mental_health_gdf.plot(column="low_access", legend=True, ax=ax31)
ax31.set_title("Low Mental Health Provider Access Counties in NC")

fig3.savefig(
    "30_results/figures/figA8_low_access_binary_map.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig3)


# figure 4: rucc categories for low access counties
fig4, ax41 = plt.subplots()
low_access.plot(column="rucc_category", legend=True, ax=ax41)
ax41.set_title("RUCC Categories for Low Mental Health Provider Access Counties in NC")

fig4.savefig(
    "30_results/figures/figA6_rucc_map.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig4)
# export high and low access data
low_access.reset_index(drop=True).to_file(
    "20_intermediate_files/high_access_gdf.geojson", driver="GeoJSON"
)

low_access.reset_index(drop=True).to_file(
    "20_intermediate_files/low_access_gdf.geojson", driver="GeoJSON"
)
