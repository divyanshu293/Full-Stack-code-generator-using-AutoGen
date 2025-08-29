# 🧩 Multi-Agent Code Generation System  

This project implements a **multi-agent system** that transforms **Software Requirements Specification (SRC)** documents into fully functional **Angular + FastAPI applications**.  
It leverages **AutoGen**, **local LLMs (via LM Studio/Ollama)**, **Streamlit UI**, and **FastAPI backend** to orchestrate specialized agents for requirements analysis, backend generation, frontend generation, testing, and code review — all with **human-in-the-loop validation**.  

---

## 🚀 Features
- **Requirements Analysis Agent**  
  - Parses PDFs/DOCX/Markdown SRC files.  
  - Generates two SRDs (`srd_backend.md`, `srd_frontend.md`).  
  - Flags **ambiguities, contradictions, and duplicates**.  

- **Backend Agent Workflow**  
  - Designs **FastAPI endpoints** + OpenAPI schemas.  
  - Generates **Pydantic models**.  
  - Implements **business logic & integrations**.  
  - Creates **Alembic migration scripts**.  

- **Frontend Agent Workflow**  
  - Generates **Angular components, services, and NgRx state management**.  
  - Implements **UI flows & SCSS styles**.  
  - Ensures **responsive design & accessibility**.  

- **Testing & Code Review Agents**  
  - Scaffolds **pytest, integration, and E2E tests**.  
  - Performs **security & performance checks**.  
  - Flags **OWASP vulnerabilities, N+1 queries, code smells**.  

- **Human-in-the-Loop Workflow**  
  - Approve or request revisions after each stage.  
  - Manual editing of SRDs & generated code in UI.  
  - Rollback mechanism if agent output fails.  

---


## ⚙️ Tech Stack
- **Orchestration**: [AutoGen](https://microsoft.github.io/autogen/)  
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)  
- **Frontend (UI)**: [Streamlit](https://streamlit.io/)  
- **Frontend (Generated App)**: [Angular 19 + NgRx]  
- **Database Migrations**: [Alembic]  
- **Testing**: Pytest, FastAPI TestClient, Cypress (E2E)  
- **Local LLMs**:  
  - [DeepSeek-Coder-6.7B GGUF](https://huggingface.co/deepseek-ai/deepseek-coder-6.7b-instruct) (backend code)  
  - [CodeLlama-7B Instruct GGUF](https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF) (frontend code)  
  - [Phi-3-mini](https://huggingface.co/microsoft/phi-3-mini-4k-instruct) (lightweight reasoning)  

---

## 🔧 Setup Instructions

### 1️⃣ Clone Repo
```bash
git clone https://github.com/divyanshu293/multi-agent-codegen.git
cd multi-agent-codegen
