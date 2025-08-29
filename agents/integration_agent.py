from config.configs import Config
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

SYSTEM_MESSAGE = """
You are an **Integration Agent**.
Your job is to:
- Integrate APIs with frontend and backend services.
- Ensure smooth data flow between client, server, and database.
- Handle cross-cutting concerns (auth, logging, error handling).
"""

def get_integration_agent():
    llm_config = {
        "config_list": [{
                "model": "deepseek-coder-1.3b-kexer",   # friendly alias
                "base_url": "http://localhost:1234/v1",  # LM Studio endpoint
                "api_type": "openai",          # LM Studio mimics OpenAI API
                "api_key": "lm-studio",        # Put any dummy string, but NOT the URL
            }],
        "temperature": 0.2,
    }
    return MultimodalConversableAgent(
        name="IntegrationAgent",
        system_message=SYSTEM_MESSAGE,
        llm_config=llm_config,
    )
