from src.models import get_model
from src.prompts.prompt import load_prompt
from src.tools.tool import get_tools

from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

_tools = get_tools()
# _chat_model = get_model().bind_tools(_tools)
_chat_model = get_model()
_prompt = load_prompt("spell_agent")


graph = create_react_agent(_chat_model, tools=_tools, prompt=_prompt)


if __name__ == "__main__":
    image = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(image)
