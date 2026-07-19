"""
****************************************************************************
PROJECT: AI_Engineering_Digital_Signal_Telemetry
PHASE: Phase 12 - N-Tier Python Sidecar Integration
LAYER: Intelligence Tier (Python Sidecar)
FILENAME: intelligence_sidecar.py
BASELINE: intelligence_sidecar_WORKING.txt
VERSION: CPU ONLY
****************************************************************************
"""

# ---------------------------------------------------------------------------
# STANDARD LIBRARY IMPORTS
# ---------------------------------------------------------------------------
import os
import sys
import time
from pathlib import Path
from typing import List

# ---------------------------------------------------------------------------
# THIRD-PARTY IMPORTS
# ---------------------------------------------------------------------------
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

import chromadb
from chromadb.config import Settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# PYTHON PACKAGE ROOT / PATHS
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from python.paths import PROJECT_ROOT, RAG_DB_ROOT, FINETUNE_MODEL_ROOT  # type: ignore

# ---------------------------------------------------------------------------
# CPU-ONLY GLOBALS (Transformers 5.x)
# ---------------------------------------------------------------------------
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TRANSFORMERS_NO_CUDA"] = "1"
torch.cuda.is_available = lambda: False
torch.backends.mps.is_available = lambda: False

# ---------------------------------------------------------------------------
# MODEL SELECTION FLAG (3B vs 8B)
# ---------------------------------------------------------------------------
BASE_MODEL_KEY = "llama-3.2-3b"   # default; UI selects actual model

# ---------------------------------------------------------------------------
# ABSOLUTE MODEL PATHS (HF-formatted, non-blob)
# ---------------------------------------------------------------------------
LLAMA_3_2_3B_PATH = (
    "D:/DEVELOPMENT/Projects/AI_Engineering_Digital_Signal_Telemetry/"
    "models/llama-3.2-3b"
)

LLAMA_3_1_8B_PATH = (
    "D:/DEVELOPMENT/Projects/AI_Engineering_Digital_Signal_Telemetry/"
    "models/llama-3.1-8b-instruct"
)

PHI3_MINI_PATH = (
    "D:/DEVELOPMENT/Projects/AI_Engineering_Digital_Signal_Telemetry/"
    "models/phi3-mini"
)

# ---------------------------------------------------------------------------
# MODEL PATH REGISTRY
# ---------------------------------------------------------------------------
MODEL_PATHS = {
    "llama-3b-fast": PHI3_MINI_PATH,      # Phi-3 Mini (fast)
    "llama-3.2-3b": LLAMA_3_2_3B_PATH,    # Llama 3.2 3B Instruct
    "llama-3.1-8b": LLAMA_3_1_8B_PATH,    # Llama 3.1 8B Instruct
}

# ---------------------------------------------------------------------------
# OFFLOAD DIRECTORIES (PER MODEL)
# ---------------------------------------------------------------------------
OFFLOAD_DIRS = {
    "llama-3b-fast": Path(__file__).parent / "offload" / "offload_llama_3b_fast",
    "llama-3.2-3b": Path(__file__).parent / "offload" / "offload_llama_3_2_3b",
    "llama-3.1-8b": Path(__file__).parent / "offload" / "offload_llama_3_1_8b",
}

OFFLOAD_DIR = OFFLOAD_DIRS[BASE_MODEL_KEY]
OFFLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# RAG DATABASE PATH
# ---------------------------------------------------------------------------
VECTOR_DB_PATH = str(RAG_DB_ROOT)

# ---------------------------------------------------------------------------
# AVAILABLE MODELS / ADAPTERS (INTERNAL KEYS)
# ---------------------------------------------------------------------------
AVAILABLE_MODELS = [
    "llama-3b-fast",          # Phi-3 Mini
    "llama-3.2-3b",           # Llama 3.2 3B Instruct
    "llama-3.1-8b",           # Llama 3.1 8B Instruct
]

AVAILABLE_ADAPTERS = [
    "default-lora",
    "telemetry-diagnostics-lora",
]

# ---------------------------------------------------------------------------
# UI → INTERNAL MODEL / ADAPTER MAPPINGS
# ---------------------------------------------------------------------------
MODEL_MAP = {
    "Llama-3B (Fast)": "llama-3b-fast",
    "Llama-3.2-3B (Instruct)": "llama-3.2-3b",
    "Llama-3.1-8B (Instruct)": "llama-3.1-8b",
}

ADAPTER_MAP = {
    "None": "default-lora",
    "DMR Troubleshooting": "telemetry-diagnostics-lora",
    "P25 adapter": "telemetry-diagnostics-lora",
    "NXDN adapter": "telemetry-diagnostics-lora",
}

# ---------------------------------------------------------------------------
# ADAPTER PATHS — MUST MATCH FINETUNE OUTPUT DIRS
# ---------------------------------------------------------------------------
ADAPTER_PATHS = {
    "default-lora": None,
    "telemetry-diagnostics-lora": {
        "llama-3b-fast": str(
            PROJECT_ROOT / "models" / "finetune_engine_phase11_3b" / "checkpoint-5"
        ),
        "llama-3.2-3b": str(
            PROJECT_ROOT / "models" / "finetune_engine_phase11_llama_3_2_3b" / "checkpoint-5"
        ),
        "llama-3.1-8b": str(
            PROJECT_ROOT / "models" / "finetune_engine_phase11_llama_3_1_8b" / "checkpoint-8"
        ),
    },
}

# ---------------------------------------------------------------------------
# GLOBAL OVERRIDE — FORCE ADAPTER LOAD FOR ALL MODELS (3B, 3.2B, 8B)
# ---------------------------------------------------------------------------

FORCE_ADAPTER_LOAD = True

# ---------------------------------------------------------------------------
# CHROMA NAME
# ---------------------------------------------------------------------------
CHROMA_COLLECTION_NAME = "radio_cases"

# ---------------------------------------------------------------------------
# LAZY MODEL STATE (CPU ONLY)
# ---------------------------------------------------------------------------
_device = "cpu"

_current_model_key: str | None = None
_current_adapter_key: str | None = None
_model = None
_tokenizer = None

# ---------------------------------------------------------------------------
# CURRENT GENERATION PARAMETERS (FOR UI DISPLAY)
# ---------------------------------------------------------------------------
_current_temperature: float = 0.2
_current_top_k: int = 40
_current_top_p: float = 0.9
_current_max_new_tokens: int = 256

def _resolve_model_path(model_key: str) -> str:
    try:
        return MODEL_PATHS[model_key]
    except KeyError:
        raise ValueError(f"Unknown model key: {model_key}")

# ---------------------------------------------------------------------------
# DTO MODELS — MUST MATCH .NET DTOs
# ---------------------------------------------------------------------------

class PromptRequest(BaseModel):
    prompt: str
    modelName: str
    adapterName: str
    temperature: float
    topK: int
    topP: float
    useRag: bool
    useAgentic: bool


class PromptResponse(BaseModel):
    outputText: str
    tokenCount: int
    inferenceLatencyMs: float
    modelUsed: str
    adapterUsed: str


class RagQueryRequest(BaseModel):
    queryText: str
    topK: int


class RagChunkDto(BaseModel):
    chunkText: str
    caseId: str


class RagSimilarityScoreDto(BaseModel):
    value: float
    isHighConfidence: bool


class RagCaseMetadataDto(BaseModel):
    caseId: str
    protocolFamily: str
    symptom: str
    environment: str
    hardware: str


class RagResultDto(BaseModel):
    retrievedChunks: List[RagChunkDto]
    similarityScores: List[RagSimilarityScoreDto]
    caseMetadata: List[RagCaseMetadataDto]


class AgenticContextChunk(BaseModel):
    chunkText: str
    caseId: str


class AgenticRequest(BaseModel):
    prompt: str
    ragContext: List[AgenticContextChunk]
    modelName: str
    adapterName: str


class AgenticStepDto(BaseModel):
    stepDescription: str
    evidence: str
    intermediateConclusion: str


class AgenticResultDto(BaseModel):
    steps: List[AgenticStepDto]
    finalDiagnosis: str
    confidenceScore: float


class HealthResponse(BaseModel):
    status: str
    models_loaded: List[str]


class ModelParametersResponse(BaseModel):
    modelName: str
    adapterName: str
    temperature: float
    topK: int
    topP: float
    maxNewTokens: int
    device: str

# ---------------------------------------------------------------------------
# FASTAPI APP SETUP
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AI_Engineering_Digital_Signal_Telemetry — Intelligence Sidecar",
    version="1.0.0",
    description="Inference + RAG + Agentic backend for the .NET Dashboard",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# CHROMADB INITIALIZATION
# ---------------------------------------------------------------------------

_chroma_client = chromadb.PersistentClient(
    path=VECTOR_DB_PATH,
    settings=Settings(anonymized_telemetry=False),
)

_collection = _chroma_client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

# ---------------------------------------------------------------------------
# ADAPTER RESOLUTION / COMPATIBILITY
# ---------------------------------------------------------------------------

def is_adapter_compatible(model_key: str, adapter_key: str) -> bool:
    mk = model_key.lower()
    ak = adapter_key.lower()

    if "telemetry" in ak:
        if "llama-3.2-3b" in mk:
            return True
        if "llama-3.1-8b" in mk:
            return True
        return False

    if "default" in ak:
        return True

    if "phi3" in mk:
        return False

    return False


def resolve_adapter_path(model_key: str, adapter_key: str) -> str | None:
    if adapter_key not in ADAPTER_PATHS:
        return None

    mapping = ADAPTER_PATHS[adapter_key]
    if mapping is None:
        return None

    return mapping.get(model_key, None)


def apply_adapter_if_available(model_key: str, adapter_key: str):
    global _model

    if FORCE_ADAPTER_LOAD:
        adapter_path = resolve_adapter_path(model_key, adapter_key)
        if adapter_path is None:
            print(f"[Sidecar] OVERRIDE → No adapter path found for {model_key} + {adapter_key}. Using base model.")
            return _model

        print(f"[Sidecar] OVERRIDE → Forcing adapter load: {adapter_path}")

        try:
            _model = PeftModel.from_pretrained(
                _model,
                adapter_path,
                device_map={"": "cpu"},
            )
            _model.set_adapter(adapter_key)
            return _model
        except Exception as ex:
            print(f"[Sidecar] OVERRIDE ERROR applying adapter: {ex}")
            print("[Sidecar] Falling back to base model.")
            return _model

    if not is_adapter_compatible(model_key, adapter_key):
        print(f"[Sidecar] Incompatible model/adapter → {model_key} + {adapter_key}. Using base model only.")
        return _model

    adapter_path = resolve_adapter_path(model_key, adapter_key)
    if adapter_path is None:
        print(f"[Sidecar] Using BASE MODEL ONLY → {model_key}")
        return _model

    print(f"[Sidecar] Applying LoRA adapter → {adapter_key} @ {adapter_path}")

    try:
        _model = PeftModel.from_pretrained(
            _model,
            adapter_path,
            device_map={"": "cpu"},
        )
        _model.set_adapter(adapter_key)
        return _model
    except Exception as ex:
        print(f"[Sidecar] ERROR applying adapter: {ex}")
        print("[Sidecar] Falling back to base model.")
        return _model

# ---------------------------------------------------------------------------
# MODEL LOADING + ADAPTER APPLICATION
# ---------------------------------------------------------------------------

def load_model_if_needed(model_key: str, adapter_key: str) -> None:
    global _current_model_key, _current_adapter_key, _model, _tokenizer

    if (
        _current_model_key == model_key
        and _current_adapter_key == adapter_key
        and _model is not None
        and _tokenizer is not None
    ):
        return

    model_path = _resolve_model_path(model_key)

    _tokenizer = AutoTokenizer.from_pretrained(model_path)
    if _tokenizer.pad_token is None:
        _tokenizer.pad_token = _tokenizer.eos_token
    _tokenizer.padding_side = "left"

    base = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map={"": "cpu"},
        dtype=torch.float32,
    )

    _model = base.eval()
    _current_model_key = model_key

    _model = apply_adapter_if_available(model_key, adapter_key)
    _current_adapter_key = adapter_key

# ---------------------------------------------------------------------------
# INFERENCE ROUTING (CPU-ONLY, LAZY-LOAD)
# ---------------------------------------------------------------------------

def _select_model_and_tokenizer(model_key: str, adapter_key: str):
    load_model_if_needed(model_key, adapter_key)
    return _model, _tokenizer


def run_inference(
    prompt: str,
    model_name: str,
    adapter_name: str,
    temperature: float,
    top_k: int,
    top_p: float,
    use_rag: bool,
    use_agentic: bool,
) -> PromptResponse:

    global _current_temperature, _current_top_k, _current_top_p, _current_max_new_tokens
    global _current_model_key, _current_adapter_key

    model_key = MODEL_MAP.get(model_name, model_name)
    adapter_key = ADAPTER_MAP.get(adapter_name, adapter_name)

    model, tokenizer = _select_model_and_tokenizer(model_key, adapter_key)

    # Track current parameters for Dashboard UI
    _current_temperature = temperature
    _current_top_k = top_k
    _current_top_p = top_p
    _current_max_new_tokens = 256
    _current_model_key = model_key
    _current_adapter_key = adapter_key

    start = time.perf_counter()

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
    )

    do_sample = True
    if model_key == "mistral-7b-reasoning":
        do_sample = False

    generation_kwargs = {
        "max_new_tokens": 256,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "do_sample": do_sample,
        "pad_token_id": tokenizer.pad_token_id,
        "eos_token_id": tokenizer.eos_token_id,
        "renormalize_logits": True,
    }

    with torch.no_grad():
        output_ids = _model.generate(
            **inputs,
            **generation_kwargs,
        )

    generated_ids = output_ids[0][inputs["input_ids"].shape[1]:]
    output_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

    latency_ms = (time.perf_counter() - start) * 1000.0
    token_count = int(len(generated_ids))

    return PromptResponse(
        outputText=output_text.strip(),
        tokenCount=token_count,
        inferenceLatencyMs=float(latency_ms),
        modelUsed=model_name,
        adapterUsed=adapter_name,
    )

# ---------------------------------------------------------------------------
# RAG VECTOR RETRIEVAL
# ---------------------------------------------------------------------------

def _distance_to_similarity(distance: float) -> float:
    return 1.0 / (1.0 + distance)


def query_rag_vector_db(query_text: str, top_k: int) -> RagResultDto:
    result = _collection.query(
        query_texts=[query_text],
        n_results=top_k,
    )

    documents = result.get("documents", [[]])[0]
    distances = result.get("distances", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    ids = result.get("ids", [[]])[0]

    retrieved_chunks: List[RagChunkDto] = []
    similarity_scores: List[RagSimilarityScoreDto] = []
    case_metadata: List[RagCaseMetadataDto] = []

    for idx in range(len(documents)):
        doc = documents[idx]
        dist = float(distances[idx]) if idx < len(distances) else 1.0
        meta = metadatas[idx] if idx < len(metadatas) else {}
        case_id = meta.get("caseId") or (ids[idx] if idx < len(ids) else f"CASE-{idx}")

        retrieved_chunks.append(
            RagChunkDto(
                chunkText=str(doc),
                caseId=str(case_id),
            )
        )

        similarity = _distance_to_similarity(dist)
        similarity_scores.append(
            RagSimilarityScoreDto(
                value=similarity,
                isHighConfidence=similarity > 0.85,
            )
        )

        case_metadata.append(
            RagCaseMetadataDto(
                caseId=str(case_id),
                protocolFamily=str(meta.get("protocolFamily", "Unknown")),
                symptom=str(meta.get("symptom", "Unknown")),
                environment=str(meta.get("environment", "Unknown")),
                hardware=str(meta.get("hardware", "Unknown")),
            )
        )

    return RagResultDto(
        retrievedChunks=retrieved_chunks,
        similarityScores=similarity_scores,
        caseMetadata=case_metadata,
    )

# ---------------------------------------------------------------------------
# AGENTIC REASONING LOOP (CPU-ONLY, LAZY-LOAD)
# ---------------------------------------------------------------------------

def _parse_agentic_output(output_text: str) -> tuple[list[AgenticStepDto], str, float]:
    lines = [l.strip() for l in output_text.splitlines() if l.strip()]
    steps: list[AgenticStepDto] = []
    current_step_desc = None
    current_evidence = None
    current_conclusion = None
    final_diagnosis = ""
    confidence_score = 0.0

    for line in lines:
        lower = line.lower()
        if lower.startswith("step "):
            if current_step_desc or current_evidence or current_conclusion:
                steps.append(
                    AgenticStepDto(
                        stepDescription=current_step_desc or "",
                        evidence=current_evidence or "",
                        intermediateConclusion=current_conclusion or "",
                    )
                )
            parts = line.split(":", 1)
            current_step_desc = parts[1].strip() if len(parts) > 1 else line
            current_evidence = None
            current_conclusion = None
        elif lower.startswith("evidence:"):
            parts = line.split(":", 1)
            current_evidence = parts[1].strip() if len(parts) > 1 else ""
        elif lower.startswith("intermediate conclusion:"):
            parts = line.split(":", 1)
            current_conclusion = parts[1].strip() if len(parts) > 1 else ""
        elif lower.startswith("final diagnosis:"):
            parts = line.split(":", 1)
            final_diagnosis = parts[1].strip() if len(parts) > 1 else ""
        elif lower.startswith("confidence:"):
            parts = line.split(":", 1)
            raw_conf = parts[1].strip() if len(parts) > 1 else "0.0"
            try:
                confidence_score = float(raw_conf)
            except ValueError:
                confidence_score = 0.0

    if current_step_desc or current_evidence or current_conclusion:
        steps.append(
            AgenticStepDto(
                stepDescription=current_step_desc or "",
                evidence=current_evidence or "",
                intermediateConclusion=current_conclusion or "",
            )
        )

    if not steps:
        steps = [
            AgenticStepDto(
                stepDescription="Diagnostic reasoning step",
                evidence="Telemetry evidence",
                intermediateConclusion="Intermediate conclusion",
            )
        ]
    if not final_diagnosis:
        final_diagnosis = "Diagnosis not explicitly stated; review telemetry and context."
    if confidence_score <= 0.0:
        confidence_score = 0.5

    return steps, final_diagnosis, confidence_score


def run_agentic_reasoning(
    prompt: str,
    rag_context: List[AgenticContextChunk],
    model_name: str,
    adapter_name: str,
) -> AgenticResultDto:

    model_key = MODEL_MAP.get(model_name, model_name)
    adapter_key = ADAPTER_MAP.get(adapter_name, adapter_name)

    model, tokenizer = _select_model_and_tokenizer(model_key, adapter_key)

    context_str = "\n".join(
        f"- Case {c.caseId}: {c.chunkText}" for c in rag_context
    ) or "No RAG context provided."

    agentic_prompt = (
        "You are a senior digital radio diagnostics engineer.\n"
        "Use the telemetry context and user prompt to perform a multi-step diagnostic reasoning process.\n"
        "Respond with clearly labeled steps and a final diagnosis.\n\n"
        "Telemetry Context:\n"
        f"{context_str}\n\n"
        "User Prompt:\n"
        f"{prompt}\n\n"
        "Format your answer as:\n"
        "Step 1: <description>\n"
        "Evidence: <evidence>\n"
        "Intermediate conclusion: <conclusion>\n"
        "Step 2: ...\n"
        "Final diagnosis: <diagnosis>\n"
        "Confidence: <0.0-1.0>\n"
    )

    inputs = tokenizer(
        agentic_prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
    )

    with torch.no_grad():
        output_ids = _model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.2,
            top_k=40,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    generated_ids = output_ids[0][inputs["input_ids"].shape[1]:]
    output_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

    steps, final_diagnosis, confidence_score = _parse_agentic_output(output_text)

    return AgenticResultDto(
        steps=steps,
        finalDiagnosis=final_diagnosis,
        confidenceScore=float(confidence_score),
    )

# ---------------------------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="Active",
        models_loaded=AVAILABLE_MODELS,
    )

# ---------------------------------------------------------------------------
# MODEL PARAMETERS ENDPOINT
# ---------------------------------------------------------------------------

@app.get("/api/v1/model/parameters", response_model=ModelParametersResponse)
def get_model_parameters() -> ModelParametersResponse:
    return ModelParametersResponse(
        modelName=_current_model_key or BASE_MODEL_KEY,
        adapterName=_current_adapter_key or "default-lora",
        temperature=_current_temperature,
        topK=_current_top_k,
        topP=_current_top_p,
        maxNewTokens=_current_max_new_tokens,
        device=_device,
    )

# ---------------------------------------------------------------------------
# ENDPOINT 1: STANDARD INFERENCE
# ---------------------------------------------------------------------------

@app.post("/api/v1/inference", response_model=PromptResponse)
def standard_inference(request: PromptRequest) -> PromptResponse:

    internal_model = MODEL_MAP[request.modelName]
    internal_adapter = ADAPTER_MAP[request.adapterName]

    response = run_inference(
        prompt=request.prompt,
        model_name=internal_model,
        adapter_name=internal_adapter,
        temperature=request.temperature,
        top_k=request.topK,
        top_p=request.topP,
        use_rag=request.useRag,
        use_agentic=request.useAgentic,
    )
    return response

# ---------------------------------------------------------------------------
# ENDPOINT 2: RAG VECTOR RETRIEVAL
# ---------------------------------------------------------------------------

@app.post("/api/v1/rag/query", response_model=RagResultDto)
def rag_query(request: RagQueryRequest) -> RagResultDto:
    result = query_rag_vector_db(
        query_text=request.queryText,
        top_k=request.topK,
    )
    return result

# ---------------------------------------------------------------------------
# ENDPOINT 3: AGENTIC REASONING LOOP
# ---------------------------------------------------------------------------

@app.post("/api/v1/agentic/reason", response_model=AgenticResultDto)
def agentic_reason(request: AgenticRequest) -> AgenticResultDto:

    internal_model = MODEL_MAP[request.modelName]
    internal_adapter = ADAPTER_MAP[request.adapterName]

    result = run_agentic_reasoning(
        prompt=request.prompt,
        rag_context=request.ragContext,
        model_name=internal_model,
        adapter_name=internal_adapter,
    )
    return result

# ---------------------------------------------------------------------------
# UVICORN ENTRYPOINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "intelligence_sidecar:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )




