from beam_capacity import utilisation


def build_review_table(load_rows: list, section_lookup: dict) -> list:
    output = []
    for row in load_rows:
        section = section_lookup[row["section_name"]]
        util = round(utilisation(row, section), 2)
        output.append(
            {
                "member_id": row["member_id"],
                "combination": row["combination"],
                "utilisation": util,
                "status": "PASS" if util < 1.0 else "FAIL",
            }
        )
    output.sort(key=lambda item: item["utilisation"])
    return output[:1]
