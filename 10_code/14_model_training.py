import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

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

mental_health_df = pd.read_csv("20_intermediate_files/clean_mh_dataset.csv")

rucc_dummies = pd.get_dummies(mental_health_df["rucc_category"], drop_first=True)

mental_health_df = pd.concat([mental_health_df, rucc_dummies], axis=1)

threshold = mental_health_df["providers_per_100k"].median()

high_access = mental_health_df[mental_health_df["providers_per_100k"] >= threshold]

low_access = mental_health_df[mental_health_df["providers_per_100k"] < threshold]

high_access.reset_index(drop=True).to_csv(
    "20_intermediate_files/high_access.csv", index=False
)

low_access.reset_index(drop=True).to_csv(
    "20_intermediate_files/low_access.csv", index=False
)


predictors = [
    "unemployment_rate",
    "uninsured",
    "access_to_exercise",
    "social_associations_per_10k",
    "air_pollution",
    "log_median_hh_income",
    "mid",
    "rural",
]

# create y and X
X = high_access[predictors]
y = high_access["observed_distress"]

# split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=541
)

distress_lm = LinearRegression()
distress_lm.fit(X_train, y_train)

y_pred = distress_lm.predict(X_test)

print("R2:", r2_score(y_test, y_pred))
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("RMSE:", rmse)

residuals = y_test - y_pred

fig1, ax1 = plt.subplots()
ax1.scatter(y_pred, residuals)
ax1.axhline(0)
ax1.set(
    xlabel="Predicted",
    ylabel="Residuals",
    title="Model Residuals (High-Access Counties)",
)

fig1.savefig(
    "30_results/figures/figA4_model_residuals.png", dpi=300, bbox_inches="tight"
)
plt.close(fig1)

fig2, ax2 = plt.subplots()
ax2.scatter(y_test, y_pred)
ax2.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()])
ax2.set(
    xlabel="Actual",
    ylabel="Predicted",
    title="Observed versus Predicted Mental Health Distress (Test Sample)",
)

fig2.savefig(
    "30_results/figures/figA5_model_test_fit.png", dpi=300, bbox_inches="tight"
)
plt.close(fig2)


# now try with all high access data to get the best possible estimates before applying it to low-access counties

full_lm = LinearRegression()
full_lm.fit(X, y)

high_access["predicted_distress"] = full_lm.predict(X)


print(
    "R2:", r2_score(high_access["observed_distress"], high_access["predicted_distress"])
)

# plot to see how well our model predicted the high access counties
fig3, ax3 = plt.subplots()

ax3.scatter(
    high_access["observed_distress"],
    high_access["predicted_distress"],
    color="darkviolet",
)

min_val = min(
    high_access["observed_distress"].min(), high_access["predicted_distress"].min()
)
max_val = max(
    high_access["observed_distress"].max(), high_access["predicted_distress"].max()
)

ax3.plot([min_val, max_val], [min_val, max_val], color="gray", linestyle="--")

ax3.set(
    xlabel="Actual Distress",
    ylabel="Predicted Distress",
    title="Observed versus Predicted Mental Health Distress (Full High-Access Sample)",
)

fig3.savefig(
    "30_results/figures/fig2_model_validation_high_access.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig3)

import joblib

joblib.dump(full_lm, "20_intermediate_files/distress_model.pkl")
joblib.dump(predictors, "20_intermediate_files/model_features.pkl")
