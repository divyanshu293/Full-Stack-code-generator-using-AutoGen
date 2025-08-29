from config.configs import Config
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

SYSTEM_MESSAGE = """
You are a **Frontend Component Designer Agent**.
Your job is to:
- Convert UI requirements into Angular components.
- Generate reusable, styled, and modular UI elements.
- Follow accessibility and responsive design practices.
- write the robust code.
"""

def get_component_designer_agent():
    llm_config = {
        "config_list": [
            {
                "model": "deepseek-coder-1.3b-kexer",   # friendly alias
                "base_url": "http://localhost:1234/v1",  # LM Studio endpoint
                "api_type": "openai",          # LM Studio mimics OpenAI API
                "api_key": "lm-studio",        # Put any dummy string, but NOT the URL
            }
        ],
        "temperature": 0.25,
    }
    return MultimodalConversableAgent(
        name="ComponentDesigner",
        system_message=SYSTEM_MESSAGE,
        llm_config=llm_config,
    )