# 🧠 HOWTO — Local QLoRA Finetuning  
### AI_Engineering_Digital_Signal_Telemetry  
### RAW Markdown Reference Guide  
### Single Fenced Block

---

# 🎯 Purpose

This guide explains how to finetune a local LLM (Llama 3B or Llama 8B) using your `finetune_cases.jsonl` file.  
The finetuning process teaches the model **how to reason** about digital radio troubleshooting cases using domain‑specific instruction‑response pairs.

**QLoRA Definition:**  
**QLoRA (Quantized Low‑Rank Adaptation)** is a memory‑efficient finetuning method that applies low‑rank updates to a **4‑bit quantized base model**, enabling high‑quality training on local hardware with significantly reduced VRAM requirements.  
It is ideal for running Llama 3B and 8B finetuning on consumer GPUs or CPU‑only systems.

---

# 🧱 Requirements

You must have:

- A local Llama **3B** or **8B** model  
- The Phase 9 output file: `finetune_cases.jsonl`  
- The Python finetuning engine: `run_phase11_finetune()`  
- The output directory: `models/finetune_engine_phase11/`

---

# 📂 Directory Structure

Your working directories should look like:
