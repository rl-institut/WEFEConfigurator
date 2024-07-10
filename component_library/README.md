# Component library

The components are located under data/elements

A script should run and look which entries are available for each type, then reverse the order to obtain a mapping of the category of each available component

The scripts in scripts/utils.update_typemap.py will be run to add the required components Facades if they do not belong to the builtin ones of oemof_tabular

The following columns could be added to each component:
- description
- verbose name
