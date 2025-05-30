from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph.graph import CompiledGraph


def create_agent(chat_model: BaseChatModel, tools: list[BaseTool], prompt: str) -> CompiledGraph:
    pass
