from config.configs import Config
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
 
SYSTEM_MESSAGE = """
You are a world-class software requirements analyst. Your task is to analyze the provided source requirements document (SRD) and generate two separate, detailed technical specification documents: one for the backend and one for the frontend.
 
When you have completed the analysis and the user approves, reply with only the word "TERMINATE".
 
Your output MUST strictly be two markdown documents.
 
**Backend SRD (`srd_backend.md`)**
- **API Endpoints**: Define all necessary RESTful API endpoints.
- **Data Models**: Specify Pydantic models for all data structures.
- **Business Logic**: Detail the core business rules.
- **Technical Dependencies**: List required external services and databases.
- **Migration Plans**: Note any data migration or API versioning plans.
 
**Frontend SRD (`srd_frontend.md`)**
- **UI Components**: Describe required UI components.
- **Services**: Detail Angular services for API communication.
- **State Management**: Outline the NgRx store structure.
- **User Workflows**: Describe key user interaction flows.
 
**Analysis Rules:**
1.  **Identify Contradictions**: Explicitly flag contradictory requirements.
2.  **Identify Duplicates**: Note duplicated requirements.
3.  **Identify Ambiguities**: Highlight unclear requirements.
 
Begin your analysis now.
"""
 
def get_requirements_analyzer_agent():
    """Returns an AssistantAgent configured for requirements analysis using the llm_config pattern."""
 
    llm_config = {
        "config_list": [
            {
                "model": "deepseek-coder-1.3b-kexer",   # friendly alias
                "base_url": "http://localhost:1234/v1",  # LM Studio endpoint
                "api_type": "openai",          # LM Studio mimics OpenAI API
                "api_key": "lm-studio",        # Put any dummy string, but NOT the URL
            }
        ],
        "temperature": 0.1,
    }
 
    assistant = MultimodalConversableAgent(
        name="RequirementsAnalyzer",
        system_message=SYSTEM_MESSAGE,
        llm_config=llm_config,
     
    )
    return assistant
