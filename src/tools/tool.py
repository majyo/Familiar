from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool

from src import MODELS_DIR, MEMORY_DIR

_spell_memory_path = MEMORY_DIR / "spell_memory.json"
_embedding_model = HuggingFaceEmbeddings(model_name=str(MODELS_DIR / "bge-m3"))
_spell_memory = InMemoryVectorStore.load(_spell_memory_path, _embedding_model)

@tool()
def retrieve_spell_tool(query: str, k: int = 20) -> list:
    """
    Retrieve the most relevant spell tools based on the query.

    Args:
        query (str): The query to search for.
        k (int): The number of results to return. Default is 5.

    Returns:
        list: A list of relevant spells, each represented as a JSON string of a spell.
    """
    docs = _spell_memory.similarity_search(query, k=k)
    spells = [doc.page_content for doc in docs]
    return spells


def get_tools():
    """
    Get the list of tools available in the tool module.

    Returns:
        list: A list of tools.
    """
    return [retrieve_spell_tool]
