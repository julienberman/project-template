import pandas as pd

def clean_text(text: pd.Series) -> pd.Series:
    return text.str.replace(r'[^a-zA-Z]', '', regex=True).str.lower()
