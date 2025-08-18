# Component library

The components are located under data/elements

A script should run on the WIP_components folder and look which entries are available for each type, then reverse the order to obtain a mapping of the category of each available component

The scripts in scripts/utils.update_typemap.py will be run to add the required components Facades if they do not belong to the builtin ones of oemof_tabular

The following columns could be added to each component:
- description
- verbose name

## Trying out locally
Install requirements in a virtual environement `pip install -r component_library/scripts/requirements.txt`

## Check the validity of the component library

From within `component_library/scripts` run `python utils.py`, this will display the list of the available components and to which csv file they are linked. In case of addition of new csv files, one need to delete the `component_library/WIP_components/datapackage.json` file. You will then enounter errors like `The resource energy_sources has the following casting errors: Field "profile" can't cast value "ghi-profile" for type "integer" with format "default"` --> simply change the type to "string" for this field

### Adding new components

When you add a new component in the component library, make sure the field which should be updated by the survey has the correct type in the `component_library/WIP_components/datapackage.json`


## Postprocessing of the survey

Get questions of the survey from the database: run `python manage.py save_survey_answers <scenario number>`. This will save the answers in a json file in the format : `scenario_<scenario number>_survey_answers.json`

in `app/` run `generate_answer_mapping.py` to get the generic answer mapping file `survey_answer_component_mapping.json` and the subquestion mapping file`sub_question_mapping.json`

Those files are automatically linked in the `scripts/build_scenario.py` script.

At the very end of the file you can input the survey answers file you want to process

Run the example `python component_library/scripts/build_scenario.py`, you should see a new scenario folder named "test_scenario" under "scenarios"

## Work to fill `survey_answer_component_mapping.json`

The current structure is the following for adding a component

    "question id": {
        "map_to": "component"
        "map_answer": {
            filled with value pairs 
            "<survey answer>": "<unique type/name of component such a listed in one of the WIP_components csv>"
        }
    }

And for changing the attribute of a component

    "question id": {
        "map_to": "attribute"
        "map_answer": {
            "attribute name": "float"
        }
    },

Currently one question can only change one attribute of a component (check that...), but can add mmultiple components