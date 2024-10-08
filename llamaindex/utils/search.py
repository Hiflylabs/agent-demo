from tavily import TavilyClient


def search_web_tool(query: str, tavily: TavilyClient) -> str:
    """
    Searches the web for additional information.

    Args:
        query (str): The user's query.
        tavily (TavilyClient): Tavily client for processing the web search.

    Returns:
        str: Retrieved information from the web.
    """

    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=5,
        topic="news",
        include_raw_content=False,
        include_answer=True,
    )

    return response["answer"]
