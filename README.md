# Langgraph & LlamaIndex Agent Demo

This project demonstrates the usage of **Langgraph** and **LlamaIndex** agents, showcasing how they can make intelligent decisions based on input queries and call the appropriate tools when necessary.

## Project Structure

The project is organized into two main folders: **langraph** and **llamaindex**, each containing a Jupyter notebook and utility files for their respective agents.

```
├── README.md
├── langraph
│   ├── LanggraphAgentDemo.ipynb
│   └── utils
│       ├── agent.py
│       ├── prompts.py
│       ├── router.py
│       └── tools.py
├── llamaindex
│   ├── ReActAgentDemo.ipynb
│   └── utils
│       ├── prompts.py
│       ├── retrieval.py
│       └── search.py
└── requirements.txt
```

## Dependencies & Tech Stack

- **Langraph & LlamaIndex**: Core libraries for creating and managing agents and workflows. Langraph supports state-based workflows, while LlamaIndex enables ReAct agent decision-making and tool integration.
- **OpenAI GPT-4o**: Utilized for natural language understanding and question-answering capabilities.
- **Azure Cognitive Search**: Stores and retrieves Tesla-related financial documents to provide agents with specific data for complex queries.
- **Tavily**: Adds an additional layer of web-based data retrieval for external searches, enhancing the agent’s ability to answer broader questions.
- **Environment Variables**: Managed via a `.env` file to securely store API keys and configuration details.

For a detailed list of Python dependencies, refer to the `requirements.txt` file.

## [Langgraph Agent Demo](langraph)

In the **LanggraphAgentDemo.ipynb**, we demonstrate a classifier agent using Langgraph to handle the following:

- **Classification**: The agent first determines if a question is general or if it requires additional information from an internet search or a vector database.
- **Tool-Calling**: If additional information is required, the agent invokes a tool-calling node that can either search the web or retrieve data from a vector store.
- **Answering Questions**: If the question is general, the agent uses a chatbot to provide an answer.

### Components

- **Agents**: Three agents are created—`classifier_agent`, `chat_agent`, and `tool_using_agent`.
- **Tools**: Two tools are available—`search_web_tool` for web search and `retriever_tool` for vector store retrieval.
- **Workflow**: The workflow is set up in a state graph where the agent determines the path based on the question type.
- **Memory Persistence**: Memory is used to persist the state between graph runs using `MemorySaver`.


## [LlamaIndex ReAct Agent Demo](llamaindex)

In **ReActAgentDemo.ipynb**, we create a generalized example of a ReAct Agent using LlamaIndex with decision-making capability:

- **Classification**: The ReAct agent first prompted to determine whether it can answer a question directly or needs external information.
- **Tool-Calling**: If necessary, the agent calls other tools to either search the web or retrieve data from an Azure Cognitive Search.
- **Answering Questions**: If the agent can answer directly, it responds without calling external tools.

### Components

- **Agents**: The ReAct agent is created using `ReActAgent.from_tools`, with memory buffering and callback management.
- **Tools**: The tools available are `search_tool`, and `retriever_tool`.
- **Callback & Memory Management**: Token counting and debugging are handled by `CallbackManager`, and conversation history is stored in `ChatMemoryBuffer`.