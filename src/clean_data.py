import pandas as pd
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
LOGS = ROOT / "logs"

logging.basicConfig(
    filename=LOGS / "clean_data_log.txt",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filemode="w"
)

logging.info("Starting cleaning and filtering script")

df = pd.read_csv(DATA / "formatted_data.csv")
logging.info(f"Formatted data imported successfully. Initial shape: {df.shape}")

if "ORG_AIRPORT" not in df.columns:
    raise ValueError("ORG_AIRPORT column not found in formatted_data.csv")

original_rows = df.shape[0]

df = df[df["ORG_AIRPORT"] == "DFW"].copy()
logging.info(f"Filtered to DFW departures. Rows before: {original_rows}, rows after: {df.shape[0]}")

if df.empty:
    raise ValueError("No DFW departure records found after filtering")

print(df.head())
print(df.shape)
print(df["ORG_AIRPORT"].unique())

rows_before_duplicates = df.shape[0]
df = df.drop_duplicates()
duplicates_removed = rows_before_duplicates - df.shape[0]

logging.info(f"Duplicate rows removed: {duplicates_removed}")
print(f"Duplicates removed: {duplicates_removed}")

rows_before_na = df.shape[0]
df = df.dropna()
na_removed = rows_before_na - df.shape[0]

logging.info(f"Rows with missing values removed: {na_removed}")
print(f"N/A removed: {na_removed}")

final_airports = df["ORG_AIRPORT"].unique()

if len(final_airports) != 1 or final_airports[0] != "DFW":
    raise ValueError("Final dataset contains airports other than DFW")

df.to_csv(DATA / "cleaned_data.csv", index=False)

logging.info(f"cleaned_data.csv exported successfully. Final shape: {df.shape}")
logging.info("Final airport validation passed: only DFW departures remain")
logging.info("Cleaning and filtering script completed successfully")