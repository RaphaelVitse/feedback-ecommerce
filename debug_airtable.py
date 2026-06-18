from pyairtable import Api
import os
from dotenv import load_dotenv
from src.google_sheets import get_feedbacks

load_dotenv()
api = Api(os.getenv("AIRTABLE_TOKEN"))
table = api.table(os.getenv("AIRTABLE_BASE_ID"), os.getenv("AIRTABLE_TABLE_NAME"))

# Timestamps dans Airtable
existing = table.all(fields=["timestamp"])
existing_timestamps = {r["fields"].get("timestamp") for r in existing}
print("Airtable timestamps:", list(existing_timestamps)[:3])

# Timestamps dans Google Sheets
df = get_feedbacks()
print("Sheets timestamps:", df["timestamp"].tolist()[:3])
