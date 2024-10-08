import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from typing import Literal, TypedDict


# This defines the object that is passed between each node
# in the graph. We will create different nodes for each agent and tool
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str


def classifier_router(state: AgentState) -> Literal["SPECIFIC", "GENERAL"]:
    """
    Router to use in conditional edges after the results of the classifier agent.
    """
    last_message = state["messages"][-1]
    if "SPECIFIC" in last_message.content:
        # An agent decided the work is done
        return "SPECIFIC"
    elif "GENERAL" in last_message.content:
        return "GENERAL"
    raise Exception("The message did'nt contain SPECIFIC OR GENERAL keywords.")
