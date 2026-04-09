from load_factors import factored_line_load


def design_moment_kNm(row: dict) -> float:
    w_uls = factored_line_load(row)
    return w_uls * row["span_m"] ** 2 / 8.0


def major_axis_resistance_kNm(section: dict) -> float:
    return section["Wpl_y_cm3"] * section["fy_MPa"] / 1e6


def utilisation(row: dict, section: dict) -> float:
    return design_moment_kNm(row) / major_axis_resistance_kNm(section)
