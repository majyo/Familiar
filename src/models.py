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


if __name__ == "__main__":
    from langchain_huggingface import HuggingFaceEmbeddings

    embed_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    vector = embed = embed_model.embed_query("This is a test sentence.")
    print(vector)
