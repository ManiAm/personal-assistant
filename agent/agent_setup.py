
import logging
from typing import Annotated, TypedDict, Sequence
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages

import config

log = logging.getLogger(__name__)
load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def print_tools(tools):

    for tool in tools:
        print(f"\n>>>> Tool: {tool.name}")
        print(f"Description: {tool.description}")


async def get_tools():

    client = MultiServerMCPClient({
        "home": {
            "transport": "streamable_http",
            "url": config.home_mcp_url
        },
        "airbnb": {
            "transport": "stdio",
            "command": "npx",
            "args": [
                "-y",
                "@openbnb/mcp-server-airbnb"
            ]
        }
    })

    tools = await client.get_tools()
    print_tools(tools)

    return tools


async def build_agent():

    tools = await get_tools()

    llm = ChatOpenAI(
        model=config.llm_model,
        base_url=config.lite_llm_url
    ).bind_tools(tools)

    def model_call(state: AgentState) -> AgentState:

        system_prompt = SystemMessage(content=config.prompt)
        input_messages = [system_prompt] + state["messages"]
        response = llm.invoke(input_messages)
        return {"messages": [response]}

    def should_continue(state: AgentState):

        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"
        return "end"

    graph = StateGraph(AgentState)

    graph.add_node("my_agent", model_call)
    graph.add_node("tools", ToolNode(tools=tools))

    graph.add_edge(START, "my_agent")
    graph.add_edge("tools", "my_agent")

    graph.add_conditional_edges("my_agent", should_continue, {
        "continue": "tools",
        "end": END
    })

    app = graph.compile()
    # app.get_graph().draw_png("agent_ReAct.png")

    return app
