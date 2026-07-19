import requests
import json

payload = {
    "queryText": "DMR radio loses sync when RSSI drops below threshold",
    "topK": 5
}

response = requests.post(
    "http://localhost:8000/api/v1/rag/query",
    json=payload
)

print("STATUS:", response.status_code)
print("RESPONSE:", json.dumps(response.json(), indent=2))
