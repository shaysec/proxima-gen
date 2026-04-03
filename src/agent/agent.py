from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_ollama import ChatOllama
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from src.tools.tools import agent_tools

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize LLM (Ensure Ollama is running llama3)
llm = ChatOllama(model="llama3", temperature=0)
llm_with_tools = llm.bind_tools(agent_tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(agent_tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

agent_executor = graph_builder.compile()