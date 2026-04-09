RESULT_COLUMNS = [
    "Member",
    "Section",
    "Utilisation_ULS",
    "Status",
]


def normalise_columns(df):
    return df.rename(columns=str.strip)
