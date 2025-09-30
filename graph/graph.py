from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from langchain_core.prompts import ChatPromptTemplate
import asyncio

class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    context: list

def gen_get_context_node(v_store):
    async def get_context(state: GraphState):
        def search_v_store(prompt):
            return v_store.similarity_search(prompt, k=2)
        return {'context': await asyncio.to_thread(search_v_store, state['messages'][-1].content)}
    return get_context

def gen_call_llm_node(llm):
    async def call_llm(state: GraphState):
        return {'messages': [await (ChatPromptTemplate([('system', 'You are a helpful AI assistant! Always make security check using sql_db_security_checker before executing a query with sql_db_query.'
                                                                   'Always use duckduckgo_results_json in the case of the questions without context.'
                                                                   'Provided context is: {context}'),
                                                        ('placeholder', '{messages}')]) | llm).ainvoke(state)]}
    return call_llm

def gen_graph(v_store, llm, tools):
    graph_builder = StateGraph(GraphState)
    
    graph_builder.add_node('rag', gen_get_context_node(v_store))
    graph_builder.add_node('agent', gen_call_llm_node(llm))
    graph_builder.add_node('tools', ToolNode(tools))
    
    graph_builder.add_edge(START, 'rag')
    graph_builder.add_edge('rag', 'agent')
    graph_builder.add_edge('tools', 'agent')
    
    graph_builder.add_conditional_edges('agent', lambda state: 'tools' if state['messages'][-1].tool_calls else END, ['tools', END])
    
    return graph_builder.compile()
