from config.configs import Config
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

SYSTEM_MESSAGE = """
You are a **UI Implementation Agent**.
Your job is to:
- Implement Angular pages using designed components.
- Manage routing, layouts, and state bindings.
- Ensure performance and maintainability.
"""

def get_ui_implementation_agent():
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
        name="UIImplementationAgent",
        system_message=SYSTEM_MESSAGE,
        llm_config=llm_config,
    )
