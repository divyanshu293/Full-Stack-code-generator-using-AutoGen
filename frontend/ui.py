import streamlit as st
import requests
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import autogen
 
import requests


st.title("Streamlit + FastAPI Integration")


import sys, os

# Ensure project root is in sys.path no matter where we run from
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    project_root = Path(__file__).parent.parent
    env_path = project_root / ".env"
    load_dotenv(dotenv_path=env_path)
except Exception:
    load_dotenv()
 
# from config.configs import Config
from agents.requirements_agent import get_requirements_analyzer_agent
from agents.api_designer_agent import get_api_designer_agent
from agents.model_development_agent import get_model_developer_agent
from agents.business_logic_agent import get_business_logic_agent
from agents.integration_agent import get_integration_agent
from agents.db_migration_agent import get_db_migration_agent
from agents.component_designer_agent import get_component_designer_agent
from agents.service_development_agent import get_service_developer_agent
from agents.ui_implementation_agent import get_ui_implementation_agent
from agents.state_management_agent import get_state_management_agent
from agents.critic_agent import get_critic_agent
 
WORKFLOW_STEPS = [
    {"name": "API Designer", "agent_func": get_api_designer_agent, "output_file": "backend/api_routes.py"},
    {"name": "Model Developer", "agent_func": get_model_developer_agent, "output_file": "backend/models.py"},
    {"name": "Business Logic Developer", "agent_func": get_business_logic_agent, "output_file": "backend/business_logic.py"},
    {"name": "Integration Developer", "agent_func": get_integration_agent, "output_file": "backend/integrations.py"},
    {"name": "Database Migrator", "agent_func": get_db_migration_agent, "output_file": "backend/migration.py"},
    {"name": "Component Designer", "agent_func": get_component_designer_agent, "output_file": "frontend/component.ts"},
    {"name": "Service Developer", "agent_func": get_service_developer_agent, "output_file": "frontend/service.ts"},
    {"name": "UI Implementer", "agent_func": get_ui_implementation_agent, "output_file": "frontend/ui.html_scss"},
    {"name": "State Manager", "agent_func": get_state_management_agent, "output_file": "frontend/state.ts"},
]
MAX_RETRIES = 3
 
# State Initialization
def initialize_state():
    if "messages" not in st.session_state: st.session_state.messages = []
    if "srd_generation_complete" not in st.session_state: st.session_state.srd_generation_complete = False
    if "initial_srd_text" not in st.session_state: st.session_state.initial_srd_text = ""
    if "workflow_started" not in st.session_state: st.session_state.workflow_started = False
    if "current_step" not in st.session_state: st.session_state.current_step = 0
    if "generated_code" not in st.session_state: st.session_state.generated_code = {}
    if "current_code_to_review" not in st.session_state: st.session_state.current_code_to_review = ""
    if "critic_feedback" not in st.session_state: st.session_state.critic_feedback = ""
    if "retry_count" not in st.session_state: st.session_state.retry_count = 0
 
initialize_state()
 
# Async Helper
def run_async(async_func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(async_func(*args))
 
# Main Application UI
st.title("SRD and Code Generation with Agent Workflows")
 
if not st.session_state.srd_generation_complete:
    st.header("Phase 1: Requirements Analysis")
    user_proxy_phase1 = autogen.UserProxyAgent(name="SRD_UserProxy", code_execution_config=False)
    analyzer_agent = get_requirements_analyzer_agent()
 
    # async def run_srd_agent_turn(history):
    #     response_content = await analyzer_agent.a_generate_reply(messages=history, sender=user_proxy_phase1)
    #     # The return from a_generate_reply is the content itself, so we wrap it
    #     return {"content": response_content, "role": "assistant"}
    async def run_srd_agent_turn(history):
        response_content = await analyzer_agent.a_generate_reply(
          messages=history, sender=user_proxy_phase1
        )

    # Ensure it's a string (some backends return dict/Message objects)
        if isinstance(response_content, dict):
           response_content = response_content.get("content", str(response_content))
        elif not isinstance(response_content, str):
           response_content = str(response_content)

        return {"content": response_content, "role": "assistant"}
    uploaded_file = st.file_uploader("Upload a requirements document", type=["pdf", "docx", "md"], disabled=len(st.session_state.messages) > 0)
   
    if uploaded_file and not st.session_state.messages:
        with st.spinner('Parsing file and initiating analysis...'):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post("http://127.0.0.1:8000/upload/", files=files)
                response.raise_for_status()
                raw_text = response.json().get("raw_text", "")
 
                initial_message = {"content": f"Analyze these requirements:\n\n{raw_text}", "role": "user"}
                st.session_state.messages.append(initial_message)
                ai_response = run_async(run_srd_agent_turn, st.session_state.messages)
                st.session_state.messages.append(ai_response)
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {e}")
 
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
 
    last_message_content = st.session_state.messages[-1].get("content", "") if st.session_state.messages else ""
    if "TERMINATE" in last_message_content:
        st.success("Initial SRD analysis is complete and approved!")
        st.session_state.initial_srd_text = st.session_state.messages[-2].get("content", "")
        st.session_state.srd_generation_complete = True
        st.rerun()
 
    if st.session_state.messages and "TERMINATE" not in last_message_content:
        prompt = st.chat_input("Provide feedback or type 'approve' to finish analysis...")
        if prompt:
            st.session_state.messages.append({"content": prompt, "role": "user"})
            ai_response = run_async(run_srd_agent_turn, st.session_state.messages)
            st.session_state.messages.append(ai_response)
            st.rerun()
 


elif st.session_state.srd_generation_complete:
    st.header("Phase 2: Multi-Agent Code Generation")
    with st.expander("View Approved SRD", expanded=False):
        st.markdown(st.session_state.initial_srd_text)
   
    user_proxy_phase2 = autogen.UserProxyAgent(name="CodeGenerationProxy", code_execution_config=False)
 
    if not st.session_state.workflow_started:
        if st.button("▶️ Start Code Generation Workflow"):
            st.session_state.workflow_started = True
            st.rerun()
 
    if st.session_state.workflow_started and st.session_state.current_step < len(WORKFLOW_STEPS):
        step_config = WORKFLOW_STEPS[st.session_state.current_step]
        st.subheader(f"Step {st.session_state.current_step + 1}: {step_config['name']} (Attempt {st.session_state.retry_count + 1}/{MAX_RETRIES + 1})")
 
        if st.session_state.retry_count > MAX_RETRIES:
            st.error(f"Maximum retries ({MAX_RETRIES}) exceeded for this step.")
        else:
            if not st.session_state.current_code_to_review:
                with st.spinner(f"{step_config['name']} is generating code..."):
                    agent = step_config['agent_func']()
                    context = st.session_state.initial_srd_text + "\n\n--- PREVIOUSLY GENERATED CODE ---\n" + "\n".join(st.session_state.generated_code.values())
                    history = [{"role": "user", "content": context}]
                    response = run_async(agent.a_generate_reply, history, user_proxy_phase2)
                   
                    st.session_state.current_code_to_review = response
                st.rerun()
           
            if st.session_state.current_code_to_review and not st.session_state.critic_feedback:
                with st.spinner("Critic Agent is reviewing the code..."):
                    critic = get_critic_agent()
                    review_prompt = f"Please review the following code...\n\n--- GENERATED CODE ---\n{st.session_state.current_code_to_review}"
                    history = [{"role": "user", "content": review_prompt}]
                    feedback = run_async(critic.a_generate_reply, history, user_proxy_phase2)
                   
                    st.session_state.critic_feedback = feedback
                st.rerun()
 
            if st.session_state.current_code_to_review and st.session_state.critic_feedback:
                st.text("Generated Code:")
                st.code(st.session_state.current_code_to_review, language="python")
                st.text("Critic's Review:")
                st.info(st.session_state.critic_feedback)
 
                prompt = st.chat_input("Type 'approve' to accept, or provide feedback for the agent to retry.")
                if prompt:
                    if "approve" in prompt.lower():
                        st.session_state.generated_code[step_config['output_file']] = st.session_state.current_code_to_review
                        output_path = Path("output") / step_config['output_file']
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, "w", encoding="utf-8") as f: f.write(st.session_state.current_code_to_review)
                        st.success(f"Code approved and saved to {output_path}")
 
                        st.session_state.current_step += 1
                        st.session_state.retry_count = 0
                        st.session_state.current_code_to_review = ""
                        st.session_state.critic_feedback = ""
                        st.rerun()
                    else:
                        st.session_state.retry_count += 1
                        st.session_state.current_code_to_review = ""
                        st.session_state.critic_feedback = ""
                        st.rerun()
 
    elif st.session_state.workflow_started:
        st.header("✅ Workflow Complete!")
        st.success("All code has been generated and saved to the 'output' folder.")
        if st.button("Start New Project"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()


# import streamlit as st
# import requests
# import asyncio
# import os
# import json
# import re
# from pathlib import Path
# from typing import Dict, Any, List, Tuple

# from dotenv import load_dotenv
# import autogen

# # -------------------------------
# # Bootstrapping / Paths / .env
# # -------------------------------
# st.set_page_config(page_title="Multi-Agent Code Generator", layout="wide")

# import sys
# ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# if ROOT_DIR not in sys.path:
#     sys.path.append(ROOT_DIR)

# try:
#     project_root = Path(__file__).parent.parent
#     env_path = project_root / ".env"
#     load_dotenv(dotenv_path=env_path)
# except Exception:
#     load_dotenv()

# # -------------------------------
# # Import your agents
# # -------------------------------
# from agents.requirements_agent import get_requirements_analyzer_agent
# from agents.api_designer_agent import get_api_designer_agent
# from agents.model_development_agent import get_model_developer_agent
# from agents.business_logic_agent import get_business_logic_agent
# from agents.integration_agent import get_integration_agent
# from agents.db_migration_agent import get_db_migration_agent
# from agents.component_designer_agent import get_component_designer_agent
# from agents.service_development_agent import get_service_developer_agent
# from agents.ui_implementation_agent import get_ui_implementation_agent
# from agents.state_management_agent import get_state_management_agent
# from agents.critic_agent import get_critic_agent

# # ======================================================================================
# # Helpers
# # ======================================================================================

# def run_async(async_func, *args):
#     """Run an async function synchronously (as you already did)."""
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(async_func(*args))

# def ensure_state():
#     """Initialize Streamlit session state."""
#     ss = st.session_state
#     ss.setdefault("messages", [])
#     ss.setdefault("srd_generation_complete", False)
#     ss.setdefault("initial_srd_text", "")
#     ss.setdefault("workflow_started", False)

#     # Round-robin specific state
#     ss.setdefault("project_state", {})              # { path: content }
#     ss.setdefault("cycle_logs", [])                 # list of logs per cycle
#     ss.setdefault("current_cycle", 0)
#     ss.setdefault("max_cycles", 5)
#     ss.setdefault("critic_feedback", "")
#     ss.setdefault("last_cycle_status", "")          # "approve" or "revise"
#     ss.setdefault("in_cycle", False)                # guard to avoid duplicate clicks
#     ss.setdefault("applied_updates_last_cycle", []) # store last applied patch list
#     ss.setdefault("round_robin_initialized", False)

# def json_from_response(text: str) -> Dict[str, Any]:
#     """
#     Extract and parse JSON object from LLM response.
#     We prefer pure JSON; fallback to best-effort extraction.
#     """
#     # Quick happy path: try direct parse
#     try:
#         return json.loads(text)
#     except Exception:
#         pass

#     # Remove code fences if present
#     text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE)

#     # Find first {...} JSON object (naive bracket matching)
#     start = text.find("{")
#     end = text.rfind("}")
#     if start != -1 and end != -1 and end > start:
#         candidate = text[start:end+1]
#         try:
#             return json.loads(candidate)
#         except Exception:
#             pass

#     # Fallback to empty structure
#     return {"updates": [], "notes": f"Could not parse JSON. Raw head: {text[:200]}..."}

# def apply_updates(project_state: Dict[str, str], updates: List[Dict[str, Any]]) -> Tuple[Dict[str, str], List[Dict[str, Any]]]:
#     """
#     Apply a list of updates to the in-memory project_state.
#     Supported actions: replace_content, append, upsert.
#     Returns (new_state, applied_updates_with_diffs)
#     """
#     new_state = dict(project_state)
#     applied = []
#     for u in updates or []:
#         path = u.get("path", "").strip()
#         action = (u.get("action") or "replace_content").strip()
#         content = u.get("content", "")
#         if not path:
#             continue

#         old = new_state.get(path, "")
#         if action == "replace_content":
#             new_state[path] = content
#         elif action == "append":
#             new_state[path] = old + ("\n" if old and not old.endswith("\n") else "") + content
#         elif action == "upsert":
#             new_state[path] = content if not old else old
#         else:
#             # Unknown action: default to replace
#             new_state[path] = content

#         applied.append({
#             "path": path,
#             "action": action,
#             "before_len": len(old),
#             "after_len": len(new_state[path]),
#         })
#     return new_state, applied

# def pretty_files_summary(project_state: Dict[str, str]) -> str:
#     if not project_state:
#         return "(empty)"
#     lines = []
#     for p, v in project_state.items():
#         lines.append(f"- {p}  ({len(v)} chars)")
#     return "\n".join(lines)

# def truncate(text: str, limit: int = 8000) -> str:
#     if len(text) <= limit:
#         return text
#     head = text[:limit//2]
#     tail = text[-limit//2:]
#     return head + "\n\n... [TRUNCATED] ...\n\n" + tail

# # ======================================================================================
# # Round-Robin Orchestration
# # ======================================================================================

# def get_round_robin_agents():
#     """Order matters. Critic runs separately after each full cycle."""
#     return [
#         ("Requirements Analyzer", get_requirements_analyzer_agent),
#         ("API Designer", get_api_designer_agent),
#         ("Model Developer", get_model_developer_agent),
#         ("Business Logic Developer", get_business_logic_agent),
#         ("Integration Developer", get_integration_agent),
#         ("Database Migrator", get_db_migration_agent),
#         ("Component Designer", get_component_designer_agent),
#         ("Service Developer", get_service_developer_agent),
#         ("UI Implementer", get_ui_implementation_agent),
#         ("State Manager", get_state_management_agent),
#     ]

# ROUND_ROBIN_PROTOCOL = """
# You are part of a multi-agent coding team working on a shared codebase represented
# as a dictionary of files -> content ("project_state"). Your role is to make focused,
# minimal, production-quality changes for your area.

# STRICT OUTPUT FORMAT (IMPORTANT):
# Return ONLY valid JSON (no markdown, no backticks), with this schema:
# {
#   "updates": [
#     {
#       "path": "string (e.g., 'backend/api_routes.py')",
#       "language": "string (e.g., 'python', 'ts', 'html', 'scss')",
#       "action": "replace_content | append | upsert",
#       "content": "string - the FULL file content if replace_content/upsert, or a chunk for append"
#     }
#   ],
#   "notes": "brief rationale; mention assumptions and TODOs if any"
# }

# Rules:
# - Make compilable, runnable code. No placeholders like '...'.
# - Respect existing files; avoid duplicating the same module in different paths.
# - Only touch what your role owns. If no change is needed, return {"updates": [], "notes": "no changes"}.
# - Keep files consistent with the SRD and current project state.
# - Prefer these canonical file paths when applicable:
#   - backend/api_routes.py
#   - backend/models.py
#   - backend/business_logic.py
#   - backend/integrations.py
#   - backend/migration.py
#   - frontend/component.ts
#   - frontend/service.ts
#   - frontend/ui.html_scss
#   - frontend/state.ts
# """

# CRITIC_PROTOCOL = """
# You are the Code Critic for a multi-agent system. Review the entire project_state
# for correctness, cohesion, security, performance, and consistency with the SRD.

# OUTPUT ONLY VALID JSON (no backticks), schema:
# {
#   "status": "approve" | "revise",
#   "feedback": "concise list of issues or 'Looks good'",
#   "updates": [
#     {
#       "path": "string",
#       "language": "string",
#       "action": "replace_content | append | upsert",
#       "content": "string"
#     }
#   ]
# }

# Rules:
# - If 'revise', propose concrete patches in 'updates' (minimal but sufficient).
# - Ensure API routes, models, business logic, frontend services/components, and state
#   agree on shapes, endpoints, and error handling.
# - Flag missing tests or env configs as notes (don't block approval unless critical).
# """

# def build_agent_prompt(role_name: str, srd_text: str, project_state: Dict[str, str]) -> str:
#     files_overview = pretty_files_summary(project_state)
#     state_json = json.dumps(project_state, ensure_ascii=False)
#     return f"""
# Role: {role_name}

# SRD (authoritative requirements):
# {truncate(srd_text, 8000)}

# Current project_state overview:
# {files_overview}

# Current project_state JSON:
# {truncate(state_json, 14000)}

# {ROUND_ROBIN_PROTOCOL}
# """

# def build_critic_prompt(srd_text: str, project_state: Dict[str, str]) -> str:
#     files_overview = pretty_files_summary(project_state)
#     state_json = json.dumps(project_state, ensure_ascii=False)
#     return f"""
# Full-project Review

# SRD (authoritative requirements):
# {truncate(srd_text, 8000)}

# Current project_state overview:
# {files_overview}

# Current project_state JSON:
# {truncate(state_json, 14000)}

# {CRITIC_PROTOCOL}
# """

# async def agent_turn(agent, role_name: str, srd_text: str, project_state: Dict[str, str], user_proxy):
#     """One agent proposes JSON updates based on the shared state."""
#     prompt = build_agent_prompt(role_name, srd_text, project_state)
#     history = [{"role": "user", "content": prompt}]
#     resp = await agent.a_generate_reply(messages=history, sender=user_proxy)
#     return json_from_response(resp)

# async def critic_turn(critic_agent, srd_text: str, project_state: Dict[str, str], user_proxy):
#     prompt = build_critic_prompt(srd_text, project_state)
#     history = [{"role": "user", "content": prompt}]
#     resp = await critic_agent.a_generate_reply(messages=history, sender=user_proxy)
#     data = json_from_response(resp)
#     status = (data.get("status") or "").lower()
#     if status not in ("approve", "revise"):
#         # Be defensive: if the model didn't follow schema, force revise with feedback
#         data["status"] = "revise"
#         data["feedback"] = "Invalid critic schema; treating as 'revise'."
#         data.setdefault("updates", [])
#     return data

# def run_round_robin_cycle(srd_text: str):
#     """Execute one full round-robin cycle across all functional agents then Critic."""

#     # Initialize agents and proxy
#     user_proxy = autogen.UserProxyAgent(name="RoundRobinProxy", code_execution_config=False)

#     chain = get_round_robin_agents()
#     critic = get_critic_agent()

#     cycle_log = []
#     applied_updates_all: List[Dict[str, Any]] = []
#     current_state = dict(st.session_state.project_state)

#     # Functional agents in sequence
#     for role_name, factory in chain:
#         agent = factory()
#         result = run_async(agent_turn, agent, role_name, st.session_state.initial_srd_text, current_state, user_proxy)
#         notes = result.get("notes", "")
#         updates = result.get("updates", [])
#         new_state, applied = apply_updates(current_state, updates)
#         current_state = new_state
#         applied_updates_all.extend(applied)
#         cycle_log.append({
#             "agent": role_name,
#             "notes": notes,
#             "applied": applied,
#         })

#     # Critic pass
#     critic_agent = critic()
#     critic_result = run_async(critic_turn, critic_agent, st.session_state.initial_srd_text, current_state, user_proxy)
#     critic_updates = critic_result.get("updates", [])
#     status = critic_result.get("status", "revise")
#     feedback = critic_result.get("feedback", "")

#     if critic_updates:
#         current_state, critic_applied = apply_updates(current_state, critic_updates)
#         applied_updates_all.extend(critic_applied)
#     else:
#         critic_applied = []

#     cycle_log.append({
#         "agent": "Critic",
#         "status": status,
#         "feedback": feedback,
#         "applied": critic_applied,
#     })

#     return current_state, cycle_log, status, feedback, applied_updates_all

# def save_project_state_to_disk(project_state: Dict[str, str], base_dir: Path = Path("output")) -> List[str]:
#     saved = []
#     for path, content in project_state.items():
#         full = base_dir / path
#         full.parent.mkdir(parents=True, exist_ok=True)
#         with open(full, "w", encoding="utf-8") as f:
#             f.write(content or "")
#         saved.append(str(full))
#     return saved

# # ======================================================================================
# # UI
# # ======================================================================================

# ensure_state()

# st.title("SRD → Round-Robin Multi-Agent Code Generator")
# st.caption("Phase 1: SRD analysis; Phase 2: round-robin agents iterate with a Critic after every cycle.")

# # -------------------------------
# # Phase 1 — SRD Analysis
# # -------------------------------
# if not st.session_state.srd_generation_complete:
#     st.header("Phase 1: Requirements Analysis")
#     user_proxy_phase1 = autogen.UserProxyAgent(name="SRD_UserProxy", code_execution_config=False)
#     analyzer_agent = get_requirements_analyzer_agent()

#     async def run_srd_agent_turn(history):
#         response_content = await analyzer_agent.a_generate_reply(messages=history, sender=user_proxy_phase1)
#         return {"content": response_content, "role": "assistant"}

#     uploaded_file = st.file_uploader("Upload a requirements document", type=["pdf", "docx", "md"], disabled=len(st.session_state.messages) > 0)

#     if uploaded_file and not st.session_state.messages:
#         with st.spinner('Parsing file and initiating analysis...'):
#             try:
#                 files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
#                 response = requests.post("http://127.0.0.1:8000/upload/", files=files)
#                 response.raise_for_status()
#                 raw_text = response.json().get("raw_text", "")

#                 initial_message = {"content": f"Analyze these requirements:\n\n{raw_text}", "role": "user"}
#                 st.session_state.messages.append(initial_message)
#                 ai_response = run_async(run_srd_agent_turn, st.session_state.messages)
#                 st.session_state.messages.append(ai_response)
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"An error occurred: {e}")

#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     last_message_content = st.session_state.messages[-1].get("content", "") if st.session_state.messages else ""
#     if "TERMINATE" in last_message_content:
#         st.success("Initial SRD analysis is complete and approved!")
#         st.session_state.initial_srd_text = st.session_state.messages[-2].get("content", "")
#         st.session_state.srd_generation_complete = True
#         st.rerun()

#     if st.session_state.messages and "TERMINATE" not in last_message_content:
#         prompt = st.chat_input("Provide feedback or type 'approve' to finish analysis...")
#         if prompt:
#             st.session_state.messages.append({"content": prompt, "role": "user"})
#             ai_response = run_async(run_srd_agent_turn, st.session_state.messages)
#             st.session_state.messages.append(ai_response)
#             st.rerun()

# # -------------------------------
# # Phase 2 — Round-Robin Generation
# # -------------------------------
# else:
#     st.header("Phase 2: Multi-Agent Round-Robin Code Generation")

#     with st.expander("View Approved SRD", expanded=False):
#         st.markdown(st.session_state.initial_srd_text)

#     # Controls
#     cols = st.columns([1, 1, 1, 4])
#     with cols[0]:
#         if st.button("▶️ Start / Continue Cycle", disabled=st.session_state.in_cycle):
#             st.session_state.in_cycle = True
#             with st.spinner(f"Running cycle {st.session_state.current_cycle + 1} ..."):
#                 new_state, cycle_log, status, feedback, applied = run_round_robin_cycle(st.session_state.initial_srd_text)

#                 st.session_state.project_state = new_state
#                 st.session_state.cycle_logs.append({
#                     "cycle": st.session_state.current_cycle + 1,
#                     "log": cycle_log
#                 })
#                 st.session_state.current_cycle += 1
#                 st.session_state.critic_feedback = feedback
#                 st.session_state.last_cycle_status = status
#                 st.session_state.applied_updates_last_cycle = applied
#             st.session_state.in_cycle = False
#             st.rerun()

#     with cols[1]:
#         approve_disabled = not st.session_state.project_state
#         if st.button("✅ Approve & Save", disabled=approve_disabled):
#             saved = save_project_state_to_disk(st.session_state.project_state, Path("output"))
#             st.success("Saved files:")
#             for p in saved:
#                 st.write(p)

#     with cols[2]:
#         if st.button("🧹 Reset Phase 2"):
#             for k in ["project_state", "cycle_logs", "current_cycle", "critic_feedback",
#                       "last_cycle_status", "applied_updates_last_cycle", "in_cycle"]:
#                 st.session_state[k] = [] if "logs" in k else (0 if "cycle" in k else ("" if "feedback" in k or "status" in k else (False if "in_cycle" in k else {})))
#             st.experimental_rerun()

#     st.markdown("---")

#     # Status
#     left, right = st.columns([2, 1])
#     with left:
#         st.subheader(f"Cycle: {st.session_state.current_cycle} / {st.session_state.max_cycles}")
#         if st.session_state.last_cycle_status:
#             tag = "✅ APPROVE" if st.session_state.last_cycle_status.lower() == "approve" else "🛠️ REVISE"
#             st.write(f"Critic status: **{tag}**")
#         if st.session_state.critic_feedback:
#             st.info(st.session_state.critic_feedback)

#     with right:
#         st.subheader("Project Files")
#         st.text(pretty_files_summary(st.session_state.project_state))

#     # Cycle Logs
#     st.subheader("Cycle Logs")
#     if not st.session_state.cycle_logs:
#         st.caption("No cycles run yet. Click **Start / Continue Cycle**.")
#     else:
#         for entry in st.session_state.cycle_logs[::-1]:
#             cidx = entry["cycle"]
#             with st.expander(f"🔁 Cycle {cidx}", expanded=False):
#                 for step in entry["log"]:
#                     agent = step.get("agent")
#                     st.markdown(f"**{agent}**")
#                     if agent == "Critic":
#                         st.write(f"Status: {step.get('status')}")
#                         st.write(step.get("feedback", ""))
#                     else:
#                         notes = step.get("notes", "")
#                         if notes:
#                             st.caption(notes)
#                     applied = step.get("applied", [])
#                     if applied:
#                         for a in applied:
#                             st.code(f"{a['action'].upper()}  {a['path']}  (len {a['before_len']} → {a['after_len']})")

#     # Show file contents (optional)
#     st.subheader("Current Files (preview)")
#     if st.session_state.project_state:
#         for path, content in st.session_state.project_state.items():
#             with st.expander(path, expanded=False):
#                 # Best-effort language guess for rendering
#                 lang = "python" if path.endswith(".py") else ("ts" if path.endswith(".ts") else ("html" if path.endswith(".html") else ("scss" if path.endswith(".scss") else "")))
#                 st.code(content, language=lang or None)
