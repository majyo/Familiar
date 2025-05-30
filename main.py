import dotenv
from langchain_core.messages import HumanMessage

from src.graph import graph

dotenv.load_dotenv()


if __name__ == '__main__':
    messages = [HumanMessage(content="..."),]
    response = graph.invoke({"messages": messages})
    for message in response["messages"]:
        message.pretty_print()
