from config.configs import Config
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

SYSTEM_MESSAGE = """
You are a **Code Critic Agent**.
Your job is to:
- Review generated frontend and backend code.
- Detect bugs, inefficiencies, or security flaws.
- Suggest improvements and enforce clean code principles (SOLID, DRY, KISS).
"""

def get_critic_agent():
    llm_config = {
        "config_list": [{
                "model": "deepseek-coder-1.3b-kexer",   # friendly alias
                "base_url": "http://localhost:1234/v1",  # LM Studio endpoint
                "api_type": "openai",          # LM Studio mimics OpenAI API
                "api_key": "lm-studio",        # Put any dummy string, but NOT the URL
            }],
        "temperature": 0.15,
    }
    return MultimodalConversableAgent(
        name="CriticAgent",
        system_message=SYSTEM_MESSAGE,
        llm_config=llm_config,
    )
