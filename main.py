import os
from pathlib import Path

import dotenv
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

from load_spell_csv import load_spells_from_csv

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
    embed_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    spells = load_spells_from_csv(Path("data\\dnd2024spell.csv"))
    spell_docs = [Document(page_content=spell.model_dump_json()) for spell in spells]
    stores = InMemoryVectorStore(embed_model)
    stores.dump("data\\memory\\spell_memory.json")
    stores.add_documents(spell_docs)
    # retriever = stores.as_retriever()
    query = "What is the casting time of Fireball?"
    results = stores.similarity_search(query, k=10)
    for result in results:
        print(result.page_content)


if __name__ == '__main__':
    test_embedding()
