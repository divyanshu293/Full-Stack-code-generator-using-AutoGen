# from config.configs import Config
# from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

# SYSTEM_MESSAGE = """
# You are a **Business Logic Agent**.
# Your job is to:
# - Implement core backend logic in FastAPI services.
# - Ensure SOLID principles, input validation, and error handling.
# - Write clean, testable, and maintainable Python code.
# """

# def get_business_logic_agent():
#     llm_config = {
#         "config_list": [{"model": "gpt-4", "api_key": Config.OPENAI_API_KEY}],
#         "temperature": 0.25,
#     }
#     return MultimodalConversableAgent(
#         name="BusinessLogicAgent",
#         system_message=SYSTEM_MESSAGE,
#         llm_config=llm_config,
#     )


from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

SYSTEM_MESSAGE = """
You are a **Business Logic Agent**.
Your job is to:
- Implement core backend logic in FastAPI services and write the robust code.
- Ensure SOLID principles, input validation, and error handling.
- Write clean, testable, and maintainable Python code.
"""

def get_business_logic_agent():
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
        name="BusinessLogicAgent",
        system_message=SYSTEM_MESSAGE,
        llm_config=llm_config,
    )
