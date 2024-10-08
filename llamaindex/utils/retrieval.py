from azure.search.documents import SearchClient
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.llms import ChatMessage, MessageRole
from utils.prompts import default_summary_prompt


def retrieval_tool(
    query: str, search_client: SearchClient, gpt_client: AzureOpenAI
) -> str:
    """
    Searches the Azure Cognitive Search for additional information and uses Azure OpenAI to generate a response.
    NOTE: For demonstration purposes this function only uses text-based search in the vector database.

    Args:
        query (str): The user's query.
        search_client (SearchClient): Search client connected to the Azure Cognitive Search service.
        gpt_client (AzureOpenAI): Azure OpenAI client to handle the chat response generation.

    Returns:
        str: Retrieved information from the search client and generated response from OpenAI.
    """

    # Perform a search on the Azure Cognitive Search index
    search_results = search_client.search(
        search_text=query, top=5
    )  # Adjust 'top' to limit the number of results

    # Collect results and format them for the prompt
    sources = []
    for result in search_results:
        content = result.get("content")
        if content:
            sources.append(f"{content} ---")

    # Join all sources into a single string for prompt injection
    formatted_sources = "\n".join(sources)
    # Create the full prompt to send to Azure OpenAI
    full_prompt = default_summary_prompt.format(sources=formatted_sources)

    # Prepare the chat messages
    messages = [
        ChatMessage(role=MessageRole.SYSTEM, content=full_prompt),
        ChatMessage(
            role=MessageRole.USER,
            content=query,  # The user query
        ),
    ]

    # Call Azure OpenAI to generate the response
    response = gpt_client.chat(messages=messages)

    # Return the content of the response from OpenAI
    return response.message.content
