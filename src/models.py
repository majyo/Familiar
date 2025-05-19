import dotenv
import os

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


def get_model() -> BaseChatModel:
    """
    Get the model name from the environment variable.
    """
    dotenv.load_dotenv()
    model_name = os.getenv("MODEL_NAME")
    base_url = os.getenv("BASE_URL")
    api_key = os.getenv("API_KEY")
    if not(model_name or base_url or api_key):
        raise ValueError("MODEL_NAME, BASE_URL, and API_KEY must be set in the environment variables.")
    return ChatOpenAI(model=model_name, base_url=base_url, api_key=api_key)
