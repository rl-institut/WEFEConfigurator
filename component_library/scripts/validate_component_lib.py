from oemof.tabular.datapackage import building
import datapackage as dp
import os

COMPONENT_TEMPLATES_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "WIP_components"))

dp_json = os.path.join(COMPONENT_TEMPLATES_PATH, "datapackage.json")

if os.path.exists(dp_json):
    print("Only inferring metadata")
    p = dp.Package(dp_json)
    building.infer_package_foreign_keys(p)
    p.descriptor["resources"].sort(key=lambda x: (x["path"], x["name"]))
    p.commit()
    p.save(dp_json)

else:
    print("Creating datapackage.json")
    building.infer_metadata_from_data(
        package_name="WEFE component library",
        path=COMPONENT_TEMPLATES_PATH,
    )

