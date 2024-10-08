from typing import Any, Union, List, Dict
from langgraph.graph.state import CompiledStateGraph
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
from langchain_core.runnables.base import RunnableSequence
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage

from utils.router import AgentState


def create_agent(
    llm: AzureChatOpenAI, default_prompt: str, tools: List = []
) -> RunnableSequence:
    """
    Create an agent with the provided prompt.
    If no tools are specified, the agent will be created without them.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", default_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))

    if tools:
        chain = prompt | llm.bind_tools(tools)
    else:
        chain = prompt | llm

    return chain  # type: ignore


def agent_node(state: AgentState, agent: RunnableSequence, name: str) -> AgentState:
    """
    Process the current state through an agent and update the state with the agent's response.

    This function invokes the given agent with the current state, processes the result,
    and updates the state with the new message. It handles both regular AIMessages and ToolMessages.

    Args:
        state (AgentState): The current state containing messages and sender information.
        agent (RunnableSequence): The agent to invoke. This is a RunnableSequence created by the
                                  create_agent function.
        name (str): The name of the agent, used to tag the response message.

    Returns:
        AgentState: The updated state with the new message added.

    Note:
        The function assumes that the agent's `invoke` method returns either an AIMessage,
        a ToolMessage, or an object that can be converted to an AIMessage.
    """
    result = agent.invoke(state)
    # If the result is from a tool, ensure it's wrapped as a ToolMessage
    if isinstance(result, ToolMessage):
        # Keep the ToolMessage as is and pass it through
        result_message = result
    else:
        # Otherwise, convert it to an AIMessage
        result_message = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        # "messages": state["messages"] + [result_message],
        "messages": [result_message],
        "sender": name,
    }


def invoke_graph(
    graph: CompiledStateGraph, messages: str | List[str], thread_id: str = "1"
) -> Union[Dict[str, Any], Any]:
    """
    Invokes a graph with a series of human messages and returns the result in a dictionary format.

    This function sends one or more human messages to a compiled state graph, invoking the graph's processing logic,
    and returns the result in a structured format, typically a dictionary. The function supports providing a single
    message or a list of messages and includes optional conversation threading via a `thread_id`.

    Args:
        graph (CompiledStateGraph): The graph object to process the input messages.
        messages (str | list[str]): The message(s) to send to the graph. Can be a single string or a list of strings.
        thread_id (str, optional): The thread ID for the conversation context. Defaults to '1'.

    Returns:
        The output of the graph run.
    """
    if isinstance(messages, list):
        configured_messages = [HumanMessage(content=message) for message in messages]
    else:
        configured_messages = [HumanMessage(content=messages)]
    config = {"configurable": {"thread_id": thread_id}}
    result = graph.invoke(input={"messages": configured_messages}, config=config)
    return result["messages"][-1].content
