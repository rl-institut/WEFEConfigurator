# All

If an attribute is supposed to be a float, then either write 0.0 instead of 0 in the value of the attribute of the components in WIP_components, or change the fields "type" in datapackage.json of WIP_components (must be redone if we regenerate the file from scratch, so I would advice to write the format of the numbers correct in the resources directly)

# Water treatment
water treatment currently is modeled with two inputs (electricity and water), however there are some solutions which do not require electricty!
TODO find solution for case that various filtration nad desalination system are put in series..;;;;;;;;;;;;;;;;;;;;;;;;
specific energy consumption eqauls  conversion_factor_ac-elec-bus (some kind of efficiency);;;;;;;;;;;;;;;;;;;;;;;;
conversion_rate_feed_bus always equals 1; could be omitted;;;;;;;;;;;;;;;;;;;;;;;

# Storage

 TODO consider modelling groundwater as storage: es, groundwater can indeed be modeled as storage.
 Groundwater storage refers to the volume of water stored in an aquifer, which can be influenced
 by factors such as recharge (inflow) and discharge (outflow) rates.
This concept is crucial for understanding and managing water resources,
 especially in regions dependent on groundwater for agriculture, drinking water, and industry.

 Groundwater models often use specific storage (SS) values to predict how groundwater levels will respond
 to various factors like pumping, recharge, and climate change2. These models help in making informed decisions
 about water management and sustainability.

# Crops
 TODO add crop types; potentially differenciate between C2 and C3 plant

 # Irrigation

 TODO find a solution to model smart irrigation

 # Load


 groundwater could also be modeled as water storage, thus groundwater recharge just recharges groundwater storage

# wastewater treatment 

currently it is modeled with two inputs (electricity and water), however there are some solutions which do not require electricty!
 TODO find solution for case that various filtration nad desalination system are put in series..;;;;;;;;;;;;;;;;;;;;;;;;
 specific energy consumption eqauls  conversion_factor_ac-elec-bus (some kind of efficiency);;;;;;;;;;;;;;;;;;;;;;;;
 conversion_rate_feed_bus always equals 1; could be omitted;;;;;;;;;;;;;;;;;;;;;;;

# Water pump

 water pumps are modeled as two inputs (electricity, water) - one output transformer (water)
 from_bus_0 = primary bus
 TODO find solution for case that various filtration nad desalination system are put in series..
 specific energy consumption eqauls  conversion_factor_ac-elec-bus (some kind of efficiency)
 conversion_rate_feed_bus always equals 1; could be omitted
 include specific throughput of the pump, [m³/kW]
 
# Water sources

 marginal cost shall equal price of tap water and water from the water truck"
 
# Desalination

conversion_factor_ac-elec-bus eqals specific energy consumption [kWh/m³]


task: provide all busses from all components in "bus.csv" check the datapackage.json and if there are no foreign key for a resource which should have busses --> add them to the bus.csv file

If you have a profile in a resource, make sure its exact name appears in one of the column of a file within data/sequences so that it will be recognized as a foreign key and added to the datapackage.