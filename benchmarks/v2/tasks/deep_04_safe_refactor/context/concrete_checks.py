from common_formatting import format_status


def concrete_utilisation(v_ed, v_rd):
    if v_rd <= 0:
        return None
    return v_ed / v_rd


def concrete_status(v_ed, v_rd):
    util = concrete_utilisation(v_ed, v_rd)
    if util is None:
        return "CHECK INPUT"
    return format_status(util)
