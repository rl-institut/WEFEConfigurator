water_treatment_train = {
    "main_list": [
        "intake_structure",
        "coarse_bar_screen",
        "fine_screen",
        "grit_chamber",
        "cartridge_filter",
        "simple_oxidation",
        "coagulation_flocculation",
        ["slow_sand_filter", "ceramic_filter", "biofiltration"], # both series/parallel possible # membrane protection
        "microfiltration",
        "ultrafiltration",
        ["activated_carbon_filter", "adsorption"], # both series/parallel possible # membrane protection
        "ion_exchange",
        "nanofiltration",
        ["electrodialysis", "reverse_osmosis"], # both series/parallel possible
        "membrane_distillation",
        ["distillation","boiling"],
        ["photocatalysis", "ozonation"],
        "biological_denitrification",
        ["slow_sand_filter", "ceramic_filter", "biofiltration"], # both series/parallel possible # polishing
        ["uv_disinfection","chlorination"], # both series/parallel possible
        "activated_carbon_filter", # polishing
    ],

    "pollutant_trains": {
        "drinking_water": {
            "decentralized": {
                "salinity": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter"],
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "membrane_distillation",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "arsenic": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "simple_oxidation", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "biofiltration"],
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    ["electrodialysis", "reverse_osmosis"],
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "lead": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter"],
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    "ion_exchange",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "mercury": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter"],
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    "ion_exchange",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "cadmium": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter"],
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    "ion_exchange",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "iron": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "simple_oxidation", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "biofiltration"],
                    "microfiltration",
                    "ultrafiltration",
                    "activated_carbon_filter",
                    ["uv_disinfection", "chlorination"]
                ],
                "pesticides": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter"],
                    "microfiltration",
                    "ultrafiltration",
                    ["photocatalysis", "ozonation"],
                    "biofiltration",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "pharmaceuticals": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter"],
                    "microfiltration",
                    "ultrafiltration",
                    ["photocatalysis", "ozonation"], # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "biofiltration",
                    "activated_carbon_filter",
                    "membrane_distillation", # deviation till here
                    ["uv_disinfection", "chlorination"]
                ],
                "fertilizers": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter"],
                    "microfiltration",
                    "ultrafiltration",
                    "biological_denitrification", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "ion_exchange",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "adsorption", # deviation till here
                    ["uv_disinfection", "chlorination"]
                ]
            },
            "centralized": {
                "salinity": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    "simple_oxidation",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter", "biofiltration"],
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "membrane_distillation",
                    "distillation",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "arsenic": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "simple_oxidation", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter", "biofiltration"],
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "membrane_distillation",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "lead": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    "simple_oxidation",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter", "biofiltration"],
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    "ion_exchange",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "membrane_distillation",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "mercury": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    ["simple_oxidation", "ozonation"], # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter", "biofiltration"],
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    "ion_exchange",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "membrane_distillation",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "cadmium": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    "simple_oxidation",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter", "biofiltration"],
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    "ion_exchange",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "membrane_distillation",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "iron": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "simple_oxidation", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "biofiltration"],
                    "microfiltration",
                    "ultrafiltration",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "pesticides": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    "simple_oxidation",
                    "coagulation_flocculation",
                    "microfiltration",
                    "ultrafiltration",
                    ["photocatalysis", "ozonation"], # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "biofiltration",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "activated_carbon_filter",
                    "membrane_distillation", # deviation till here
                    ["uv_disinfection", "chlorination"]
                ],
                "pharmaceuticals": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    "microfiltration",
                    "ultrafiltration",
                    ["photocatalysis", "ozonation"], # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "biofiltration",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "activated_carbon_filter",
                    "membrane_distillation", # deviation till here
                    ["uv_disinfection", "chlorination"]
                ],
                "fertilizers": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    "simple_oxidation",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "biofiltration"],
                    "microfiltration",
                    "ultrafiltration",
                    "biological_denitrification", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "ion_exchange",
                    "nanofiltration",
                    ["electrodialysis", "reverse_osmosis"],
                    "adsorption",
                    "membrane_distillation", # deviation till here
                    ["uv_disinfection", "chlorination"]
                ]
            }
        },
        "service_water": {
            "decentralized": {
                "salinity": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter"],
                    "microfiltration",
                    "ultrafiltration",
                    ["nanofiltration", "electrodialysis"],
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "arsenic": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "simple_oxidation", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "cartridge_filter",
                    "coagulation_flocculation",
                    "adsorption",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "lead": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    "microfiltration",
                    "ultrafiltration",
                    "ion_exchange",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "mercury": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    ["uv_disinfection", "chlorination"]
                ],
                "cadmium": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    "microfiltration",
                    "ultrafiltration",
                    "ion_exchange",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "iron": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "simple_oxidation", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["cartridge_filter", "ceramic_filter"],
                    "coagulation_flocculation",
                    ["slow_sand_filter", "biofiltration"],
                    "activated_carbon_filter",
                    ["uv_disinfection", "chlorination"]
                ],
                "pesticides": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    "activated_carbon_filter",
                    "biofiltration",
                    ["uv_disinfection", "chlorination"]
                ],
                "pharmaceuticals": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    "activated_carbon_filter",
                    "biofiltration",
                    ["uv_disinfection", "chlorination"]
                ],
                "fertilizers": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    "microfiltration",
                    "ultrafiltration",
                    "biological_denitrification", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "ion_exchange",
                    "adsorption", # deviation till here
                    ["uv_disinfection", "chlorination"]
                ]
            },
            "centralized": {
                "salinity": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    "microfiltration",
                    "ultrafiltration",
                    ["nanofiltration", "electrodialysis"],
                    "reverse_osmosis",
                    "membrane_distillation",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "arsenic": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "simple_oxidation", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "biofiltration"],
                    "adsorption",
                    ["nanofiltration", "reverse_osmosis"],
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "lead": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    "simple_oxidation",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter"],
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    "ion_exchange",
                    ["nanofiltration", "reverse_osmosis"],
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "mercury": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    ["simple_oxidation", "ozonation"], # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "coagulation_flocculation",
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    "ion_exchange",
                    ["reverse_osmosis", "membrane_distillation"],
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "cadmium": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "ceramic_filter"],
                    "microfiltration",
                    "ultrafiltration",
                    "adsorption",
                    "ion_exchange",
                    ["nanofiltration", "reverse_osmosis"],
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "iron": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "simple_oxidation", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "biofiltration"],
                    "microfiltration",
                    "ultrafiltration",
                    "activated_carbon_filter",
                    ["uv_disinfection", "chlorination"]
                ],
                "pesticides": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    "microfiltration",
                    "ultrafiltration",
                    ["photocatalysis", "ozonation"],
                    "biofiltration",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "pharmaceuticals": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    "microfiltration",
                    "ultrafiltration",
                    ["photocatalysis", "ozonation"],
                    "biofiltration",
                    "activated_carbon_filter", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    ["uv_disinfection", "chlorination"]
                ],
                "fertilizers": [
                    "intake_structure",
                    "coarse_bar_screen",
                    "fine_screen",
                    "grit_chamber",
                    "cartridge_filter",
                    "coagulation_flocculation",
                    ["slow_sand_filter", "biofiltration"],
                    "microfiltration",
                    "ultrafiltration",
                    "biological_denitrification", # functional tradeoff,
                    # sequence deviates from master/main train to account for realistic engineering design
                    "ion_exchange",
                    ["nanofiltration", "adsorption"], # deviation till here
                    ["uv_disinfection", "chlorination"]
                ]
            }
        }
    }
}