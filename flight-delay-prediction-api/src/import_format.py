import pandas as pd
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
LOGS = ROOT / "logs"

logging.basicConfig(
    filename=LOGS / "import_format_log.txt",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filemode="w"
)

logging.info("Starting import and formatting script")

df = pd.read_csv(DATA / "raw_airport_data.csv")
print(df.head())

logging.info("Raw CSV imported successfully")

df = df.rename(columns={
    "DAY_OF_MONTH": "DAY",
    "ORIGIN": "ORG_AIRPORT",
    "DEST": "DEST_AIRPORT",
    "CRS_DEP_TIME": "SCHEDULED_DEPARTURE",
    "DEP_TIME": "DEPARTURE_TIME",
    "DEP_DELAY": "DEPARTURE_DELAY",
    "CRS_ARR_TIME": "SCHEDULED_ARRIVAL",
    "ARR_TIME": "ARRIVAL_TIME",
    "ARR_DELAY": "ARRIVAL_DELAY"
})

logging.info("Columns renamed to match model requirements")

for col in df.columns:
    print(col)

df.to_csv(
    DATA / "formatted_data.csv",
    index=False
)

logging.info("Formatted data exported successfully")
logging.info("Import and formatting script completed successfully")
