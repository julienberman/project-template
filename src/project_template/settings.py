"""Project settings. For further information, see
https://docs.kedro.org/en/stable/kedro_project_setup/settings.html."""

# Manage hooks. Executed in Last-In-First-Out (LIFO) order.
from project_template.utils.hooks.ValidateData import ValidateData
HOOKS = (ValidateData(),)

# Installed plugins for which to disable hook auto-registration.
# DISABLE_HOOKS_FOR_PLUGINS = ("kedro-viz",)

# Class that manages storing KedroSession data.
# from kedro.framework.session.store import BaseSessionStore
# SESSION_STORE_CLASS = BaseSessionStore
# Keyword arguments to pass to the `SESSION_STORE_CLASS` constructor.
# SESSION_STORE_ARGS = {
#     "path": "./sessions"
# }

# Directory that holds configuration.
# CONF_SOURCE = "conf"

# Manage configuration loading.
from kedro.config import OmegaConfigLoader

CONFIG_LOADER_CLASS = OmegaConfigLoader
CONF_SOUURCE = "conf"
# Keyword arguments to pass to the `CONFIG_LOADER_CLASS` constructor.
CONFIG_LOADER_ARGS = {
      "base_env": "base",
      "default_run_env": "local",
#       "config_patterns": {
#           "spark" : ["spark*/"],
#           "parameters": ["parameters*", "parameters*/**", "**/parameters*"],
#       }
}

# Class that manages Kedro's library components.
# from kedro.framework.context import KedroContext
# CONTEXT_CLASS = KedroContext

# Class that manages the Data Catalog.
# from kedro.io import DataCatalog
# DATA_CATALOG_CLASS = DataCatalog

# Logging configuration
KEDRO_LOGGING_CONFIG = "conf/base/logging.yml"
