import pandas as pd
from kedro_datasets.pandas import CSVDataset

class ValidatedCSVDataset(CSVDataset):
    def __init__(
        self,
        filepath: str,
        keys: list = None,
        logpath: str = None,
        reorder_columns: bool = True,
        sort_by_key: bool = True,
        **kwargs
    ):
        super().__init__(filepath=filepath, **kwargs)
        self._keys = keys or []
        self._logpath = logpath
        self._reorder_columns = reorder_columns
        self._sort_by_key = sort_by_key

    def save(self, data: pd.DataFrame) -> None:
        if self._keys:
            if self._reorder_columns:
                cols = self._keys + [c for c in data.columns if c not in self._keys]
                data = data[cols]
            if self._sort_by_key:
                data = data.sort_values(self._keys)
        super().save(data)


