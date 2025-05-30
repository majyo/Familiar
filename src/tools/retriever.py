from pymilvus import MilvusClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool

from src import MODELS_DIR

DEFAULT_MILVUS_URI = "http://localhost:19530"
client = MilvusClient(DEFAULT_MILVUS_URI)
client.list_databases()
client.use_database("dnd_agent")
client.load_collection(collection_name="spells")

_embedding_model = HuggingFaceEmbeddings(model_name=str(MODELS_DIR / "bge-m3"))
# _spell_memory_path = MEMORY_DIR / "spell_memory.json"
# _spell_memory = InMemoryVectorStore.load(_spell_memory_path, _embedding_model)


@tool()
def query_spell_tool(semantic_query: str, filter_expr: str, output_fields: list[str], limit: int = 25) -> list:
    """
    Retrieve the most relevant spell tools based on the query.

    Args:
        semantic_query (str): The query to search for. Can be empty string if only filtering is needed.
        filter_expr (str): The filter expression to apply to the search. Can be empty string if no filtering is needed.
        output_fields (list[str]): The fields to return in the results.
        limit (int): The number of results to return. Default is 25.

    Returns:
        list: A list of relevant spells, each represented as a JSON string of a spell.
    """
    if semantic_query:
        query_vector = _embedding_model.embed_query(semantic_query)
        res = client.search(collection_name="spells", data=[query_vector], filter=filter_expr, output_fields=output_fields, limit=limit)
        data = []
        for hits in res:
            data += hits
    else:
        data = client.query(collection_name="spells", filter=filter_expr, output_fields=output_fields, limit=limit)
    return data
