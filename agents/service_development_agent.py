from config.configs import Config
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

SYSTEM_MESSAGE = """
You are a **Frontend Service Development Agent**.
Your job is to:
- Implement Angular services for API calls in typescript.
- Handle observables, async operations, and error management.
- Ensure type safety and modularity.
"""

def get_service_developer_agent():
    llm_config = {
        "config_list": [{
                "model": "deepseek-coder-1.3b-kexer",   # friendly alias
                "base_url": "http://localhost:1234/v1",  # LM Studio endpoint
                "api_type": "openai",          # LM Studio mimics OpenAI API
                "api_key": "lm-studio",        # Put any dummy string, but NOT the URL
            }],
        "temperature": 0.25,
    }
    return MultimodalConversableAgent(
        name="ServiceDeveloper",
        system_message=SYSTEM_MESSAGE,
        llm_config=llm_config,
    )
