import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("mode.copy_on_write", True)
import os

os.makedirs("30_results/figures", exist_ok=True)

plt.rcParams.update(
    {
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": "black",
        "axes.linewidth": 1,
        "xtick.color": "black",
        "ytick.color": "black",
    }
)

import joblib

model = joblib.load("20_intermediate_files/distress_model.pkl")
predictors = joblib.load("20_intermediate_files/model_features.pkl")

low_access = pd.read_csv("20_intermediate_files/low_access.csv")

low_access["predicted_distress"] = model.predict(low_access[predictors])

# plot actual vs predicted
fig1, ax1 = plt.subplots()

ax1.scatter(low_access["predicted_distress"], low_access["observed_distress"])

min_val = min(
    low_access["predicted_distress"].min(), low_access["observed_distress"].min()
)

max_val = max(
    low_access["predicted_distress"].max(), low_access["observed_distress"].max()
)

ax1.plot([min_val, max_val], [min_val, max_val])
ax1.set(
    xlabel="Predicted Distress",
    ylabel="Observed Distress",
    title="Observed versus Predicted Mental Health Distress (Low-Access Counties)",
)

fig1.savefig(
    "30_results/figures/figA1_low_access_actual_vs_predicted.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig1)

##
low_access["prediction_gap"] = (
    low_access["observed_distress"] - low_access["predicted_distress"]
)

## figure 2
fig2, ax2 = plt.subplots()

ax2.scatter(
    low_access["predicted_distress"], low_access["prediction_gap"], color="darkviolet"
)
ax2.axhline(0, linestyle="--", color="gray")
ax2.set(
    xlabel="Predicted Distress",
    ylabel="Observed − Predicted",
    title="Prediction Gap versus Expected Mental Health Distress",
)

fig2.savefig(
    "30_results/figures/fig4_prediction_gap_scatter.png", dpi=300, bbox_inches="tight"
)
plt.close(fig2)

## figure 3
fig3, ax3 = plt.subplots()

ax3.hist(low_access["prediction_gap"], bins=15)
ax3.axvline(0)
ax3.set(
    xlabel="Observed − Predicted",
    ylabel="Count",
    title="Distribution of Prediction Gap (Low-Access Counties)",
)

fig3.savefig(
    "30_results/figures/figA2_prediction_gap_distribution.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig3)

## figure
fig4, ax4 = plt.subplots()

colors = low_access["rucc_category"].map(
    {"metro": "blue", "mid": "green", "rural": "orange"}
)

ax4.scatter(low_access["predicted_distress"], low_access["prediction_gap"], c=colors)
ax4.axhline(0)
ax4.set(
    xlabel="Predicted Distress",
    ylabel="Observed − Predicted",
    title="Prediction Gap by Rural-Urban Classification (RUCC)",
)

import matplotlib.patches as mpatches

handles = [
    mpatches.Patch(color="blue", label="metro"),
    mpatches.Patch(color="green", label="mid"),
    mpatches.Patch(color="orange", label="rural"),
]

ax4.legend(handles=handles, title="RUCC")

fig4.savefig(
    "30_results/figures/figA3_gap_by_rucc_scatter.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig4)

# merge prediction gap data to geo dataframe
import geopandas as gpd

low_access_gdf = gpd.read_file("20_intermediate_files/low_access_gdf.geojson")
low_access_gdf = low_access_gdf.merge(
    low_access[["fips", "prediction_gap"]], on="fips", how="left"
)

## figure 5
fig5, ax5 = plt.subplots()

low_access_gdf.plot(
    column="prediction_gap",
    cmap="coolwarm_r",
    legend=True,
    legend_kwds={"shrink": 0.8, "aspect": 30},
    linewidth=0.2,
    edgecolor="black",
    ax=ax5,
)
ax5.set_axis_off()
ax5.spines["bottom"].set_linewidth(0.5)
ax5.spines["bottom"].set_linewidth(0.5)

ax5.set_title("Prediction Gap across Low-Access Counties")

fig5.savefig(
    "30_results/figures/fig3_prediction_gap_map.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig5)

## get top 5 negative
results = {}

TOP = 5
most_negative = low_access.nsmallest(TOP, "prediction_gap")
most_positive = low_access.nlargest(TOP, "prediction_gap")

results["neg_rucc_counts"] = most_negative["rucc_category"].value_counts().to_dict()
results["pos_rucc_counts"] = most_positive["rucc_category"].value_counts().to_dict()

neg_means = most_negative[
    ["unemployment_rate", "uninsured", "log_median_hh_income", "access_to_exercise"]
].mean()

pos_means = most_positive[
    ["unemployment_rate", "uninsured", "log_median_hh_income", "access_to_exercise"]
].mean()

results["neg_means"] = neg_means.to_dict()
results["pos_means"] = pos_means.to_dict()


## figure 6
top_combined = pd.concat(
    [
        most_negative.assign(group="Most Negative"),
        most_positive.assign(group="Most Positive"),
    ]
)

top_combined = top_combined.sort_values("prediction_gap")
colors = ["red" if x < 0 else "blue" for x in top_combined["prediction_gap"]]

fig6, ax6 = plt.subplots(figsize=(8, 5))

ax6.barh(top_combined["county"], top_combined["prediction_gap"], color=colors)

ax6.axvline(0, linestyle="--", color="black")

ax6.set(
    xlabel="Prediction Gap (Observed − Predicted)",
    title="Counties with Largest Positive and Negative Prediction Gaps",
)

fig6.savefig(
    "30_results/figures/fig5_top_counties_gap.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig6)

results["gap_mean"] = low_access["prediction_gap"].mean()
results["gap_by_rucc"] = (
    low_access.groupby("rucc_category")["prediction_gap"].mean().to_dict()
)

import json

with open("30_results/analysis_results.json", "w") as f:
    json.dump(results, f, indent=4)
