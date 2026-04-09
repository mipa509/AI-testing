SECTIONS = {
    "254x146x31 UB": {"Wpl_y_cm3": 366.0, "fy_MPa": 275.0},
    "305x165x40 UB": {"Wpl_y_cm3": 649.0, "fy_MPa": 275.0},
}


def get_section_properties(name: str) -> dict:
    section = SECTIONS[name]
    return {
        "fy_MPa": section["fy_MPa"],
        "Wpl_y_mm3": section["Wpl_y_cm3"] * 1e2,
    }
