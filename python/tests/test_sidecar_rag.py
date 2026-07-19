import requests
import json

url = "http://localhost:8000/api/v1/rag/query"

payload = {
    "queryText": "audio dropouts when mobile unit is moving",
    "topK": 3
}

print("Sending query to sidecar...")

response = requests.post(url, json=payload)

if response.status_code != 200:
    print("❌ ERROR:", response.status_code, response.text)
    raise SystemExit(1)

data = response.json()

print("\n------------------------------------------------------------")
print("SIDE CAR RAG RESPONSE")
print("------------------------------------------------------------")

# Retrieved chunks
print("\nRetrieved Chunks:")
for chunk in data.get("retrievedChunks", []):
    print(f"  CaseId: {chunk.get('caseId')}")
    print(f"  ChunkText: {chunk.get('chunkText')[:80]}...")

# Similarity scores
print("\nSimilarity Scores:")
for score in data.get("similarityScores", []):
    print(f"  Value: {score.get('value'):.4f}  | High Confidence: {score.get('isHighConfidence')}")

# Metadata
print("\nCase Metadata:")
for meta in data.get("caseMetadata", []):
    print(f"\n  CaseId: {meta.get('caseId')}")
    print(f"    ProtocolFamily: {meta.get('protocolFamily')}")
    print(f"    Symptom:        {meta.get('symptom')}")
    print(f"    Environment:    {meta.get('environment')}")
    print(f"    Hardware:       {meta.get('hardware')}")

print("\n------------------------------------------------------------")
print("Metadata verification complete.")
print("------------------------------------------------------------")

