import pandas as pd

from project_template.utils.process_text import clean_text

def build_iso(iso: dict, globals={}):
    start_year = globals["start_year"]
    end_year = globals["end_year"]
    years = list(range(start_year, end_year + 1))
    
    panel = (
        pd.DataFrame(list(iso.items()), columns=["country", "iso3c"])
        .assign(iso3c = lambda x: clean_text(x["iso3c"]))
        .assign(country = lambda x: clean_text(x["country"]))
        .assign(key = 1)
        .merge(pd.DataFrame({"year": years, "key": 1}), on="key")
        .drop(columns=["key"])
    )    
    return panel
    
