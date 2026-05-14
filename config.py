import os

# Disable telemetry
os.environ["OTEL_SDK_DISABLED"] = "true"

# Disable LiteLLM remote fetch
os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"

# Disable proxy issues
os.environ["NO_PROXY"] = "*"

from crewai import LLM
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Shared LLM configuration
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)