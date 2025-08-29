from config.configs import Config
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

SYSTEM_MESSAGE = """
You are a **State Management Agent**.
Your job is to:
- Implement Angular state management using NgRx or Signals.
- Handle app-wide state, caching, and sync with backend APIs.
- Ensure scalability and maintainability.
"""

def get_state_management_agent():
    llm_config = {
        "config_list": [ {
                "model": "deepseek-coder-1.3b-kexer",   # friendly alias
                "base_url": "http://localhost:1234/v1",  # LM Studio endpoint
                "api_type": "openai",          # LM Studio mimics OpenAI API
                "api_key": "lm-studio",        # Put any dummy string, but NOT the URL
            }],
        "temperature": 0.25,
    }
    return MultimodalConversableAgent(
        name="StateManagementAgent",
        system_message=SYSTEM_MESSAGE,
        llm_config=llm_config,
    )
