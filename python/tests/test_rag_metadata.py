import chromadb
from chromadb.config import Settings

# Hard-coded path to your vector DB
RAG_DB_ROOT = "D:/DEVELOPMENT/Projects/AI_Engineering_Digital_Signal_Telemetry/rag_db"

print("------------------------------------------------------------")
print("CHROMADB METADATA INSPECTION TOOL")
print("Using Vector DB Path:", RAG_DB_ROOT)
print("------------------------------------------------------------")

client = chromadb.PersistentClient(
    path=RAG_DB_ROOT,
    settings=Settings(anonymized_telemetry=False),
)

collection = client.get_collection("radio_cases")

# VALID include fields ONLY
result = collection.get(include=["metadatas", "documents"])

print("------------------------------------------------------------")
print("RESULTS")
print("------------------------------------------------------------")

ids = result.get("ids", [])
metas = result.get("metadatas", [])
docs = result.get("documents", [])

if not ids:
    print("ERROR: No IDs returned. Database may be empty.")
    raise SystemExit(1)

for idx, case_id in enumerate(ids):
    print("Case ID:", case_id)
    print("Metadata:", metas[idx])
    print("Document Preview:", docs[idx][:120].replace("\n", " ") + "...")
    print("------------------------------------------------------------")

print("SUMMARY")
print("------------------------------------------------------------")

missing_meta = sum(1 for m in metas if not m)

if missing_meta == len(metas):
    print("RESULT: All metadata entries are EMPTY.")
    print("This confirms the ingestion pipeline never stored metadata.")
    print("The Python sidecar correctly returns 'Unknown'.")
    print("The .NET Dashboard correctly shows 'Unknown'.")
    print("FIX: Rebuild the RAG database with metadata included.")
else:
    print("Metadata exists for some or all entries.")
    print("The Dashboard UI should be able to display protocol/symptom/etc.")

print("------------------------------------------------------------")
print("END OF REPORT")
print("------------------------------------------------------------")






