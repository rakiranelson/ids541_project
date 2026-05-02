# cleaning dataframe so its in a format ready for analysis

import pandas as pd
import numpy as np
import sklearn

pd.set_option("mode.copy_on_write", True)

mental_health_df = pd.read_csv("20_intermediate_files/mental_health_dataset.csv")

# drop gates county because it's missing data for mental health provider access
mental_health_df = mental_health_df.dropna(subset=["mh_providers"])

# updating column names and units
mental_health_df["providers_per_100k"] = mental_health_df["mh_providers"] * 100000

mental_health_df["log_median_hh_income"] = np.log(
    mental_health_df["median_household_income"]
)

prop_to_perc = ["uninsured", "unemployment_rate", "access_to_exercise"]

mental_health_df[prop_to_perc] = mental_health_df[prop_to_perc] * 100

mental_health_df = mental_health_df.rename(
    columns={"social_associations": "social_associations_per_10k"}
)


# categorize rucc codes
def categorize_rucc(code):
    if code <= 3:
        return "metro"
    elif code <= 6:
        return "mid"
    else:
        return "rural"


mental_health_df["rucc_category"] = mental_health_df["rucc_code"].apply(categorize_rucc)

mental_health_df["rucc_category"] = pd.Categorical(
    mental_health_df["rucc_category"],
    categories=["metro", "mid", "rural"],
    ordered=True,
)

# drop old columns
mental_health_df = mental_health_df.drop(
    columns={"mh_providers", "median_household_income", "rucc_code"}
)

mental_health_df.reset_index(drop=True).to_csv(
    "20_intermediate_files/clean_mh_dataset.csv", index=False
)
