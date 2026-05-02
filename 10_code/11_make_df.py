import pandas as pd
import numpy as np

pd.set_option("mode.copy_on_write", True)

import warnings

warnings.simplefilter("ignore", pd.errors.DtypeWarning)

"""
https://data.cdc.gov/500-Cities-Places/PLACES-County-Data-GIS-Friendly-Format-2025-releas/i46a-9kgh/about_data

https://www.countyhealthrankings.org/health-data/county-health-rankings-measures 

https://www.countyhealthrankings.org/sites/default/files/media/document/2023%20Data%20Dictionary%20%28PDF%29.pdf 

https://www.ers.usda.gov/data-products/rural-urban-continuum-codes/documentation 

"""

places_data = pd.read_csv(
    "00_source_data/PLACES__County_Data_(GIS_Friendly_Format),_2025_release_20260501.csv"
)
chr_data = pd.read_csv("00_source_data/analytic_data2023.csv")
rucc_data = pd.read_csv(
    "00_source_data/Ruralurbancontinuumcodes2023.csv", encoding="latin-1"
)


nc_places_data = places_data.loc[places_data["StateAbbr"].str.contains("NC")]

nc_chr_data = chr_data.loc[chr_data["State Abbreviation"].str.contains("NC")]

nc_rucc_data = rucc_data.loc[rucc_data["State"].str.contains("NC")]

## MHLTH_CrudePrev: Model-based estimate for crude prevalence of frequent mental health distress among adults, 2023

## Loneliness_CrudePrev:  Model-based estimate for crude prevalence of feeling socially isolated among adults, 2023

nc_places_data = nc_places_data[
    [
        "StateAbbr",
        "CountyName",
        "CountyFIPS",
        "TotalPop18plus",  # among adults
        "MHLTH_CrudePrev",
        "LONELINESS_CrudePrev",
    ]
].rename(
    columns={
        "StateAbbr": "state",
        "CountyName": "county",
        "CountyFIPS": "fips",
        "TotalPop18plus": "adult_pop",
        "MHLTH_CrudePrev": "observed_distress",
        "LONELINESS_CrudePrev": "loneliness_rate",
    }
)

# v062_rawvalue: Mental Health Providers raw value
# v132_rawvalue: Access to Exercise Opportunities raw value
# v140_rawvalue: Social Associations raw value
# v125_rawvalue: Air Pollution - Particulate Matter raw value
# v003_rawvalue: Uninsured Adults raw value
# v023_rawvalue: Unemployment raw value
# v063_rawvalue: Median Household Income raw value

nc_chr_data = nc_chr_data[
    [
        "5-digit FIPS Code",
        "Mental Health Providers raw value",
        "Access to Exercise Opportunities raw value",
        "Social Associations raw value",
        "Air Pollution - Particulate Matter raw value",
        "Uninsured Adults raw value",
        "Unemployment raw value",
        "Median Household Income raw value",
    ]
].rename(
    columns={
        "5-digit FIPS Code": "fips",
        "Mental Health Providers raw value": "mh_providers",
        "Access to Exercise Opportunities raw value": "access_to_exercise",
        "Social Associations raw value": "social_associations",
        "Air Pollution - Particulate Matter raw value": "air_pollution",
        "Uninsured Adults raw value": "uninsured",
        "Unemployment raw value": "unemployment_rate",
        "Median Household Income raw value": "median_household_income",
    }
)

# drop row that is just the state fips code
nc_chr_data = nc_chr_data.loc[~(nc_chr_data["fips"] == 37000)]

nc_rucc_data = nc_rucc_data.pivot(
    index="FIPS", columns="Attribute", values="Value"
).reset_index()

nc_rucc_data = nc_rucc_data[["FIPS", "RUCC_2023"]].rename(
    columns={"FIPS": "fips", "RUCC_2023": "rucc_code"}
)

nc_analysis_df = nc_places_data.merge(nc_chr_data, on="fips", how="inner")

nc_analysis_df = nc_analysis_df.merge(nc_rucc_data, on="fips", how="inner")


nc_analysis_df.reset_index(drop=True).to_csv(
    "20_intermediate_files/mental_health_dataset.csv", index=False
)
