# What is the `conf` folder for?

Store project-level configuration files here. This README.md file should contain instructions for how to reproduce local configuration. See the [Kedro documentation](https://docs.kedro.org/en/stable/configuration/configuration_basics.html) for specific details.

## Local configuration

The `local` folder should be used for configuration that is either user-specific (e.g. IDE configuration) or protected (e.g. security keys). Do not version control any local configuration files! This directory is intentionally left empty. Examples of files that should go in the `local` folder:

- `credentials.yml`: A registry of all login credentials to access various datasets.
- `ide.yml`: IDE configuration parameters.

## Base configuration

The `base` folder is for shared configuration, such as non-sensitive and project-related configuration that may be shared across team members. Do not put access credentials in the base configuration folder! Examples of files that should go in the `base` folder:

- `catalog.yml`: A registry of all data sources available for use by the project. Maps node inputs to node outputs. See the [Kedro documentation](https://docs.kedro.org/en/0.19.10/data/kedro_data_catalog.html).
- `logging.yml`: A configuration file for logging.
- `parameters.yml`: A registry for a project's hyperparameters, such as the sampling procedure, a random seed, or the train-test split size.
