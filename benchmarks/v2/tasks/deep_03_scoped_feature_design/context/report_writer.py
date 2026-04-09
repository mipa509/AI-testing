from io_contract import RESULT_COLUMNS


def report_rows(summary_df):
    return summary_df.loc[:, RESULT_COLUMNS].to_dict(orient="records")
