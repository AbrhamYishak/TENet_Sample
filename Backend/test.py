import coreapi
import os
from dotenv import load_dotenv

load_dotenv()

client = coreapi.Client()
schema = client.get("https://healthsites.io/api/docs/")


action = ["facilities", "list"]
params = {
    "api-key": os.environ.get("API"),
    "page": 1,
    "extent": (-179.15, 51.21, -129.97, 71.44),
}
result = client.action(schema, action, params=params)