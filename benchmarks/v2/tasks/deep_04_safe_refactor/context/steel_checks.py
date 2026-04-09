from common_formatting import format_status


def steel_utilisation(n_ed, n_rd):
    if n_rd <= 0:
        return 0.0
    return n_ed / n_rd


def steel_status(n_ed, n_rd):
    return format_status(steel_utilisation(n_ed, n_rd))
