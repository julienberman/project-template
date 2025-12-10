import pandas as pd
import janitor

from project_template.utils.process_text import clean_text

def build_gdp_nominal(gdp_nominal: pd.DataFrame, globals={}):
    start_year = globals["start_year"]
    end_year = globals["end_year"]
    panel = (
        gdp_nominal
        .dropna(axis=1, how="all")
        .clean_names()
        .drop(columns=["indicator_name", "indicator_code", "country_code"])
        .melt(id_vars=["country_name"], var_name="year", value_name="gdp_nominal")
        .rename(columns={"country_name": "country"})
        .assign(country = lambda x: clean_text(x["country"]))
        .assign(year=lambda df: df["year"].astype(int))
        .assign(gdp_nominal=lambda df: df["gdp_nominal"].astype(float))
        .dropna(subset=["year"])
        .query("@start_year <= year <= @end_year")
    )
    return panel
    
def build_gdp_ppp(gdp_ppp: pd.DataFrame, globals={}):
    start_year = globals["start_year"]
    end_year = globals["end_year"]
    panel = (
        gdp_ppp
        .dropna(axis=1, how="all")
        .clean_names()
        .drop(columns=["indicator_name", "indicator_code", "country_code"])
        .melt(id_vars=["country_name"], var_name="year", value_name="gdp_ppp")
        .rename(columns={"country_name": "country"})
        .assign(country = lambda x: clean_text(x["country"]))
        .assign(year=lambda df: df["year"].astype(int))
        .assign(gdp_ppp=lambda df: df["gdp_ppp"].astype(float))
        .dropna(subset=["year"])
        .query("@start_year <= year <= @end_year")
    )
    return panel

def build_wdi(gdp_nominal: pd.DataFrame, gdp_ppp: pd.DataFrame, iso: pd.DataFrame):
    panel = (
        iso
        .merge(gdp_nominal, on=['country', 'year'], how='left')
        .merge(gdp_ppp, on=['country', 'year'], how='left')
    )
    return panel
