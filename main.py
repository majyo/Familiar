import os
import dotenv
from langchain_openai import ChatOpenAI


dotenv.load_dotenv()


if __name__ == '__main__':
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))
    response = llm.invoke([
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ])
    print(response.content)
