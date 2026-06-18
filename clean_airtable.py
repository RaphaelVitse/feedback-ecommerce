from pyairtable import Api
import os
from dotenv import load_dotenv

load_dotenv()
api = Api(os.getenv("AIRTABLE_TOKEN"))
table = api.table(os.getenv("AIRTABLE_BASE_ID"), os.getenv("AIRTABLE_TABLE_NAME"))

# Supprime tous les enregistrements
all_records = table.all()
ids = [r["id"] for r in all_records]
table.batch_delete(ids)
print(f"{len(ids)} enregistrements supprimés ✅")
