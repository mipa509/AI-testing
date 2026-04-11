ULS_GAMMA_G = 1.35
ULS_GAMMA_Q = 1.50


def factored_line_load(row: dict) -> float:
    return (row["G_kN_per_m"] * ULS_GAMMA_G) + row["Q_kN_per_m"]
