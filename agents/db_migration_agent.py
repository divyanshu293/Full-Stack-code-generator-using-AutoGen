from config.configs import Config
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

SYSTEM_MESSAGE = """
You are a **Database Migration Agent**.
Your job is to:
- Generate migration scripts (Alembic).
- Ensure schema changes are consistent and reversible.
- Maintain compatibility with production environments.
"""

def get_db_migration_agent():
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
        name="DBMigrationAgent",
        system_message=SYSTEM_MESSAGE,
        llm_config=llm_config,
    )
