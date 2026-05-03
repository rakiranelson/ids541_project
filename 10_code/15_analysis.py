import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("mode.copy_on_write", True)
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
    title="Observed vs Predicted (Low-Access Counties)",
)

plt.tight_layout()
plt.show()

##
low_access["prediction_gap"] = (
    low_access["observed_distress"] - low_access["predicted_distress"]
)

## figure 2
fig2, ax2 = plt.subplots()

ax2.scatter(low_access["predicted_distress"], low_access["prediction_gap"])
ax2.axhline(0)
ax2.set(
    xlabel="Predicted Distress",
    ylabel="Observed − Predicted",
    title="Prediction Gap vs Expected Distress)",
)

plt.tight_layout()
plt.show()

## figure 3
fig3, ax3 = plt.subplots()

ax3.hist(low_access["prediction_gap"], bins=15)
ax3.axvline(0)
ax3.set(
    xlabel="Observed − Predicted",
    ylabel="Count",
    title="Distribution of Prediction Gap",
)

plt.tight_layout()
plt.show()

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
    title="Prediction Gap by RUCC Category",
)

import matplotlib.patches as mpatches

handles = [
    mpatches.Patch(color="blue", label="metro"),
    mpatches.Patch(color="green", label="mid"),
    mpatches.Patch(color="orange", label="rural"),
]

ax4.legend(handles=handles, title="RUCC")

plt.tight_layout()
plt.show()

# merge prediction gap data to geo dataframe
import geopandas as gpd

low_access_gdf = gpd.read_file("20_intermediate_files/low_access_gdf.geojson")
low_access_gdf = low_access_gdf.merge(
    low_access[["fips", "prediction_gap"]], on="fips", how="left"
)

## figure 5
fig5, ax5 = plt.subplots()

low_access_gdf.plot(column="prediction_gap", cmap="coolwarm_r", legend=True, ax=ax5)

ax5.set_title("Prediction Gap by County (Red = Lower Than Expected")

plt.tight_layout()
plt.show()

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

fig6, ax6 = plt.subplots(figsize=(8, 5))

ax6.barh(top_combined["county"], top_combined["prediction_gap"])

ax6.axvline(0)
ax6.set(
    xlabel="Prediction Gap (Observed − Predicted)",
    title="Counties with Largest Prediction Gaps",
)

plt.tight_layout()
plt.show()

results["gap_mean"] = low_access["prediction_gap"].mean()
results["gap_by_rucc"] = (
    low_access.groupby("rucc_category")["prediction_gap"].mean().to_dict()
)

import json

with open("30_results/analysis_results.json", "w") as f:
    json.dump(results, f, indent=4)
