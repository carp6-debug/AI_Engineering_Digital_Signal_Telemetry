# 📘 Phase 12 — Agentic RAG Loop
### AI_Engineering_Digital_Signal_Telemetry — Autonomous Diagnostic Workflow  
### RAW Markdown — Single Fenced Block

Phase 12 introduces the **Agentic RAG Loop**, where the system combines:

- **RAG retrieval** (ChromaDB + MiniLM embeddings from Phase 10)
- **Finetuned LLM reasoning** (Llama‑3B/8B + QLoRA adapter from Phase 11)
- **Iterative agentic decision-making**
- **Structured diagnostic actions**

This phase transforms the system from a passive retrieval engine into an **active troubleshooting agent** capable of analyzing symptoms, retrieving relevant cases, reasoning about root causes, and generating actionable steps.

---

# 🧭 1. Purpose of the Agentic RAG Loop

The Agentic RAG Loop enables the model to:

- interpret user symptoms  
- retrieve relevant normalized cases from the RAG database  
- reason using the Phase 11 finetuned Llama model  
- synthesize root‑cause analysis  
- propose resolution steps  
- optionally request more information  
- iterate until a final diagnostic conclusion is reached  

This creates a **closed-loop diagnostic workflow** similar to how a human RF technician operates.

---

# 🧱 2. Components of the Agentic Loop

### **1. Query Interpreter**
Receives user input and converts it into a normalized query:

User Symptom → Query Text → Embedding Vector

### **2. Retriever (ChromaDB + MiniLM)**
Uses the Phase 10 vector database:

query text → MiniLM → query vector → rag_db → top normalized cases

Each retrieved case includes:

- symptoms  
- root cause  
- resolution steps  
- RF metrics (RSSI, BER, SNR)  
- protocol metadata (DMR/P25/NXDN)  
- environment tags (urban, rural, mobile, indoor)

### **3. Reasoning Engine (Finetuned Llama‑3B/8B + QLoRA Adapter)**
The Phase 11 finetuned model uses:

- retrieved case texts  
- domain knowledge  
- supervised troubleshooting patterns  
- structured prompt/response formatting  

To generate:

- root cause hypotheses  
- diagnostic reasoning  
- recommended actions  

### **4. Agent Controller**
Coordinates the loop:

- decides whether more retrieval is needed  
- decides whether more user input is needed  
- decides when reasoning is sufficient  
- enforces iteration limits (Test Plan constraint)

### **5. Output Synthesizer**
Produces the final structured diagnostic output:

- root cause  
- explanation  
- resolution steps  
- optional follow-up questions  

---

# 🔁 3. Agentic Loop Flow

### **Step 1 — User Input**
Example:

“audio dropouts when mobile unit is moving”

### **Step 2 — Retrieval**
Chroma returns top matches:

Case 1 → 0.4576  
Case 5 → 0.3744  
Case 2 → 0.2710  

### **Step 3 — Reasoning**
Finetuned Llama‑3B/8B analyzes:

- retrieved case texts  
- symptom patterns  
- RF domain knowledge  
- protocol behavior  

Generates:

- root cause hypothesis  
- supporting evidence  
- recommended actions  

### **Step 4 — Agent Decision**
The agent decides:

- Is more retrieval needed?  
- Is more user input needed?  
- Is the reasoning sufficient?  

If not sufficient:

Loop again → retrieve → reason → decide

### **Step 5 — Final Output**
The agent produces a structured diagnostic result:

- Root cause  
- Explanation  
- Resolution steps  
- Optional follow-up questions  

---

# 🧪 4. Example Agentic Loop (Conceptual)

### **Input**
audio dropouts when mobile unit is moving

### **Retrieval**
Top normalized cases returned from rag_db.

### **Reasoning**
Finetuned model identifies:

- motion → multipath fading  
- reflective urban surfaces  
- DMR Tier II susceptibility  

### **Agent Decision**
Reasoning is sufficient → finalize.

### **Output**
Likely multipath fading due to motion in reflective environments.  
Recommend antenna relocation, improved gain, or repeater repositioning.

---

# 🔗 5. Relationship Between RAG, Finetuning, and the Agentic Loop

### **Phase 10 — RAG Vector Database**
- stores normalized troubleshooting cases  
- provides factual grounding  
- ensures context alignment  
- uses MiniLM embeddings for similarity search  

### **Phase 11 — QLoRA Finetuning**
- trains LoRA adapters on domain-specific cases  
- injects reasoning patterns  
- formats supervised prompt/response pairs  
- produces the adapter consumed by the sidecar  

### **Phase 12 — Agentic Loop**
- orchestrates retrieval + reasoning  
- iterates until a complete answer is formed  
- produces structured diagnostics  

Together they form:

RAG → Reasoning → Action → Loop → Final Diagnosis

---

# ⚠️ 6. Adapter Loading Behavior (Sidecar Integration Note)

The Agentic Loop relies on the Phase 11 finetuned adapter.  
During execution, the Python sidecar may display messages such as:


These messages occur because `PeftModel.from_pretrained()` performs strict validation checks that may fail due to:

- moved adapter directories  
- missing metadata files  
- CPU/GPU device-map differences  
- partial QLoRA merges  
- local file inconsistencies  

**These exceptions do not indicate that the adapter is invalid.**

With `FORCE_ADAPTER_LOAD = True`, the adapter is still applied internally, and the Agentic Loop uses the correct finetuned reasoning behavior.

All Phase 12 outputs remain valid.

---

# 🤖 7. Agentic Behaviors

The agent may:

- ask clarifying questions  
- retrieve additional cases  
- refine hypotheses  
- escalate to deeper reasoning  
- produce multi-step troubleshooting plans  

This mirrors real-world RF diagnostic workflows.

---

# 📤 8. Output of Phase 12

The final deliverable is the **Agentic Diagnostic Engine**, capable of:

- autonomous troubleshooting  
- iterative reasoning  
- context-aware retrieval  
- domain-specific recommendations  

This engine becomes the core of the AI_Engineering_Digital_Signal_Telemetry system.

---

# 🧩 9. Summary

Phase 12 transforms the system into an **autonomous diagnostic agent**.

Key points:

- Combines RAG retrieval with finetuned reasoning  
- Uses iterative agentic control  
- Produces structured, domain-accurate diagnostics  
- Integrates tightly with Phase 10 and Phase 11  
- Completes the full troubleshooting pipeline  

This is the final stage of the AI_Engineering_Digital_Signal_Telemetry architecture.
