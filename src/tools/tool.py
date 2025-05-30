from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool

from src import MODELS_DIR, MEMORY_DIR
from src.models import get_query_model
from src.prompts.prompt import load_prompt
from src.tools.retriever import query_spell_tool

_spell_memory_path = MEMORY_DIR / "spell_memory.json"
_embedding_model = HuggingFaceEmbeddings(model_name=str(MODELS_DIR / "bge-m3"))
_spell_memory = InMemoryVectorStore.load(_spell_memory_path, _embedding_model)

_query_llm = get_query_model().bind_tools([query_spell_tool], tool_choice="query_spell_tool")


@tool()
def retrieve_spell_tool_simple(query: str, k: int = 20) -> list:
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


@tool()
def retrieve_spell_tool(query: str) -> list:
    """
    A tool that can query relevant spells using nature language phrase.

    Args:
        query (str): The query to search for. i.e. spells a Bard can cast using a bonus action

    Returns:
        list: A list of relevant spells, each represented as a JSON string of a spell.
    """
    system_message = SystemMessage(load_prompt("query"))
    user_message = HumanMessage(query)
    response = _query_llm.invoke([system_message, user_message])
    print(response)
    if not response.tool_calls:
        return []
    tool_calls = response.tool_calls
    results = []
    for tool_call in tool_calls:
        if tool_call["name"] == "query_spell_tool":
            result = query_spell_tool.invoke(tool_call)
            results += result
    return results


def get_tools():
    """
    Get the list of tools available in the tool module.

    Returns:
        list: A list of tools.
    """
    return [retrieve_spell_tool]


if __name__ == "__main__":
    # Test the tool
    query = "查询回避侦测这个法术的详细信息。我需要了解它的作用、持续时间、以及它如何影响目标被侦测的能力。"
    result = retrieve_spell_tool(query)
    print(result)
