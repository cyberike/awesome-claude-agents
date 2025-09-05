# Project: superbuild
Generated: 2025-07-29_10-53-07

Original Task: Here’s the **revised orchestration prompt** including **voice interaction** and an **embedded UI**, while still keeping it suitable for military-grade, offline environments:

---

### 🔐 Prompt: *Build an Offline, Quantized Military AI with Voice + UI*

> **You are tasked with building a secure, offline, quantized large language model (LLM) tailored for military field deployment. The solution must include both voice input/output and an embedded UI interface. Your objectives:**
>
> ---
>
> ### 🧠 1. Base Model Selection
>
> * Select a compact, open-source LLM suitable for quantization and edge deployment (e.g., Mistral-7B, TinyLlama, Phi-2).
> * Ensure the license permits commercial and military use (Apache 2.0 preferred).
>
> ### 📚 2. Dataset Preparation
>
> * Curate a dataset using U.S. military field manuals (e.g., FM 3-21.8, FM 6-22), NATO publications, emergency protocols, rules of engagement, and tactical/leadership handbooks.
> * Clean and tokenize the dataset.
> * Prepare LoRA adapters or QLoRA layers for domain-specific fine-tuning.
>
> ### 🧮 3. Model Quantization
>
> * Quantize the fine-tuned model using GPTQ or AWQ to a format compatible with local inference (e.g., gguf, ggml, or onnx).
> * Optimize for < 6GB VRAM usage to fit on Jetson Nano, Raspberry Pi 5, or rugged laptops.
>
> ### 🗣️ 4. Voice Interface (Offline)
>
> * Integrate **Porcupine** or **Vosk** for offline wake-word and speech-to-text (STT).
> * Use **Coqui TTS**, **ElevenLabs**, or **ESPeak** (depending on hardware capability) for text-to-speech (TTS) output.
> * Include configuration to toggle voice on/off using a hardware button or command.
>
> ### 🖥️ 5. Embedded UI
>
> * Build a lightweight, **offline HTML/JS-based dashboard** or use **Tkinter / PyQt** if targeting Linux.
> * Show conversation history, allow manual text input, and include system control buttons (Restart LLM, Toggle Voice, Settings).
> * Embed LLM response confidence, token limit remaining, and system status.
>
> ### 🚀 6. Output
>
> * Save all files in /workspace/mil-assistant-v1/
> * Include:
>
>   * un_model.py to run the assistant
>   * launch_ui.py to open the embedded interface
>   * start_voice.py for voice interface startup
>   * Prebuilt quantized model file (gguf or onnx)
>   * mil-assistant-instructions.md
>   * README.md with full install and usage guide
>   * Optional: Dockerfile for easy deployment
>
> ---
>
> ### 🧭 Use Case
>
> This assistant should serve field soldiers, medics, or commanders with secure, no-internet access to doctrine, emergency support, tactical recommendations, and leadership protocols. It must respond in clear, military-style phrasing with no hallucination tolerance.
>
> ### 🧰 Constraints
>
> * 100% offline operation (no cloud APIs)
> * GPU optional but supported
> * Low RAM footprint (\~4–6GB)
> * System must boot into assistant UI automatically if installed on a Raspberry Pi, Jetson Nano, or rugged laptop
>
> Begin generation of the system now. Output real code files and organize the build in logical folders.

## Agents & Subtasks
- **AI Researcher**: 2 task(s) completed
- **Software Architect**: 1 task(s) completed
- **ML Engineer**: 3 task(s) completed
- **Voice Interface Developer**: 1 task(s) completed
- **UI/UX Developer**: 1 task(s) completed
- **DevOps Engineer**: 1 task(s) completed
