import logging
import pandas as pd
import hashlib
from pathlib import Path

from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog, MemoryDataset

class ValidateData:
    """A hook that verifies data integrity and saves a log file."""
    def __init__(self):
        self.catalog = None
    
    @property
    def _logger(self):
        return logging.getLogger(__name__)
    
    @hook_impl
    def after_catalog_created(self, catalog: DataCatalog):
        self.catalog = catalog
    
    @hook_impl
    def before_dataset_saved(self, dataset_name: str, data) -> None:
        if not isinstance(data, pd.DataFrame):
            self._logger.info(f"Skipping validation for dataset '{dataset_name}': not a pandas DataFrame...")
            return
        
        try:
            data_info = self.catalog._datasets.get(dataset_name)
        except (KeyError, AttributeError):
            self._logger.info(f"Skipping validation for dataset '{dataset_name}': not found in catalog...")
            return
        
        if isinstance(data_info, MemoryDataset):
            self._logger.info(f"Skipping validation for dataset '{dataset_name}': not a file dataset...")
            return
        
        self._logger.info(f"Validating dataset '{dataset_name}'...")
        keys = self._get_keys(dataset_name, data_info)
        self._check_columns_not_list(data)
        self._check_keys(data, keys)
        
        hash = self._generate_hash(data)
        summary_stats = self._get_summary_stats(data)
        self._save_log(dataset_name, data_info, hash, keys, summary_stats)
    
    def _check_write_to_disk(self, data_info):
        return data_info._filepath is not None
    
    def _get_keys(self, dataset_name: str, data_info):
        try:
            keys = data_info._keys
            if not isinstance(keys, list):
                raise TypeError("Keys must be specified as a list.")
            return keys
        except AttributeError:
            raise ValueError(f"Dataset '{dataset_name}' has no keys specified")
        
    def _check_columns_not_list(self, data: pd.DataFrame) -> None:
        type_list = [any(data[col].apply(lambda x: isinstance(x, list))) for col in data.columns]
        if any(type_list):
            type_list_columns = data.columns[type_list].tolist()
            raise TypeError(f"No column can be of type list. Check the following columns: `{', '.join(type_list_columns)}`")
    
    def _check_keys(self, data, keys) -> None:
        for key in keys:
            if not key in data.columns:
                raise ValueError(f"Key '{key}' not found in data columns.")
        
        df_keys = data[keys]
        
        keys_with_missing = df_keys.columns[df_keys.isnull().any()].tolist()
        if keys_with_missing:
            missings_string = ", ".join(keys_with_missing)
            raise ValueError(f"The following keys are missing in some rows: {missings_string}.")

        type_list = any([any(df_keys[keycol].apply(lambda x: isinstance(x, list))) for keycol in keys])
        if type_list:
            raise TypeError("No key can contain keys of type `list`.")

        if not all(df_keys.groupby(keys).size() == 1):
            raise ValueError("Keys do not uniquely identify the observations.")
    def _generate_hash(self, data: pd.DataFrame) -> str:
        return hashlib.md5(pd.util.hash_pandas_object(data).values).hexdigest()
    
    def _get_summary_stats(self, data: pd.DataFrame) -> pd.DataFrame:
        var_types = data.dtypes
        var_stats = (
            data
            .describe(include="all", percentiles=[0.5])
            .fillna("")
            .transpose()
            .infer_objects(copy=False)
        )
        var_stats["count"] = data.notnull().sum()
        var_stats = var_stats.drop(columns=["top", "freq"], errors="ignore")
        
        summary_stats = (
            pd.DataFrame({"type": var_types})
            .merge(var_stats, how="left", left_index=True, right_index=True)
        )
        summary_stats = summary_stats.round(4)
        
        for col in summary_stats.columns:
            if col not in ["variable_name", "type"]:
                summary_stats[col] = summary_stats[col].apply(
                    lambda x: "{:,}".format(x) if isinstance(x, int) else x
                )
                summary_stats[col] = summary_stats[col].apply(
                    lambda x: "{:,.3f}".format(x) if isinstance(x, float) else x
                )
        
        return summary_stats
    
    def _save_log(self, dataset_name: str, data_info, hash_val: str, keys: list, summary_stats: pd.DataFrame) -> None:
        filepath = Path(data_info._filepath)
        logpath = data_info._logpath
        if not logpath:
            self._logger.info(f"Omitting log file for dataset '{dataset_name}'...")
            return
        
        self._logger.info(f"Saving log file for dataset '{dataset_name}' to '{logpath}'...")
        with open(logpath, "w") as f:
            f.write(f"File: {filepath.as_posix()}\n\n")  
            f.write(f"MD5 hash: {hash_val}\n\n")
            f.write("Keys: " + " ".join(keys) + "\n\n")
            f.write(summary_stats.to_string(header=True, index=True))
            f.write("\n\n")

