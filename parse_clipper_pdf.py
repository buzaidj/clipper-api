# installed with pip install "camelot-py[base]"
# also requires dependencies that can be installed via:
#   brew install ghostscript tcl-tk
# or on Ubuntu:
#   apt install ghostscript python3-tk
import camelot
import pandas as pd


def read_clipper_pdf_to_df(path):
    tables = camelot.read_pdf(path, pages="all", flavor="stream")

    dfs = []
    for table in tables:
        df = table.df
        df.columns = [
            "TRANSACTION DATE",
            "TRANSACTION TYPE",
            "LOCATION",
            "ROUTE",
            "PRODUCT",
            "DEBIT",
            "CREDIT",
            "BALANCE",
        ]
        df["IS_VALID"] = pd.to_datetime(
            df["TRANSACTION DATE"], format="%m-%d-%Y %I:%M %p", errors="coerce"
        ).notna()
        df = df[df["IS_VALID"]]
        df = df.drop("IS_VALID", axis=1)
        dfs.append(df)

    big_df = pd.concat(dfs)
    return big_df


if __name__ == "__main__":
    path = "downloads/rideHistory_1400622187.pdf"
    print(read_clipper_pdf_to_df(path))
