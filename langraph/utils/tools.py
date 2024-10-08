from tavily import TavilyClient
from langchain_core.tools import tool
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores.azuresearch import AzureSearch
import os


@tool
def search_web_tool(query: str) -> str:
    """
    Searches the web for additional information.

    Args:
        query (str): The user's query.

    Returns:
        str: Retrieved information from the web.
    """
    # Initialize the TavilyClient inside the function
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=5,
        topic="news",
        include_raw_content=False,
        include_answer=True,
    )

    return response["answer"]


def create_vector_store_tool(vector_store: AzureSearch):
    retriever = vector_store.as_retriever()
    retriever_tool = create_retriever_tool(
        retriever,
        "retrieval_tool",
        "Search and return information about Teslas risk and revenue forecast informations",
    )
    return retriever_tool
