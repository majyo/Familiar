import os
from pathlib import Path

import dotenv
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

from load_spell_csv import load_spells_from_csv
from src.graph import graph
from src.tools.tool import retrieve_spell_tool

dotenv.load_dotenv()


def test_connection():
    llm = ChatOpenAI(model=os.getenv("MODEL_NAME"), api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))
    response = llm.invoke([
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ])
    print(response.content)


def test_embedding():
    embed_model = HuggingFaceEmbeddings(model_name="./models/bge-m3")
    spells = load_spells_from_csv(Path("data\\dnd2024spell.csv"))
    spell_docs = [Document(page_content=spell.model_dump_json()) for spell in spells]
    embedding = embed_model.embed_query(spell_docs[0].page_content)
    print(len(embedding))
    # stores = InMemoryVectorStore(embed_model)
    # stores.add_documents(spell_docs)
    # stores.dump(r"data\memory\spell_memory.json")
    # query = "What is the casting time of Fireball?"
    # results = stores.similarity_search(query, k=10)
    # for result in results:
    #     print(result.page_content)


if __name__ == '__main__':
    # messages = [HumanMessage(content="法师一环应该带哪些法术？"),]
    # response = graph.invoke({"messages": messages})
    # for message in response["messages"]:
    #     message.pretty_print()
    test_embedding()
