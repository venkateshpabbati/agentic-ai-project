---
title: LanggraphAgenticAI
emoji: 🐨
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: 1.42.0
app_file: app.py
pinned: false
license: apache-2.0
short_description: Refined langgraphAgenticAI
---

# LangGraph AgenticAI Assistant

A powerful agentic AI assistant built using LangGraph, LangChain, and Streamlit. This application enables users to interact with intelligent agents through a natural language interface, leveraging graph-based workflows for complex task automation.

## Overview

LangGraph AgenticAI Assistant is a sophisticated AI system that combines multiple AI technologies to create intelligent agents capable of handling complex tasks. The system uses LangGraph to build configurable agent workflows, allowing for flexible and dynamic interactions with users.

## Key Features

- **Smart Agent Workflows**: Leverage LangGraph's graph-based architecture for intelligent task automation
- **Natural Language Interface**: Streamlit-based UI for seamless user interactions
- **Configurable Agents**: Easily modify and extend agent behaviors through graph configurations
- **Real-time Processing**: Fast response times for interactive conversations
- **Extensible Architecture**: Support for multiple LLM providers and custom nodes
- **Robust Error Handling**: Comprehensive logging and error recovery systems

## Use Cases

- Task Automation
- Information Retrieval
- Complex Query Processing
- Multi-step Problem Solving
- Custom Agent Workflows
- Knowledge Base Interaction

## Features

- Streamlit-based web interface
- Configurable LLM integration (currently supports Groq)
- Graph-based agent workflow
- Dynamic use case support
- Real-time chat interface
- Error handling and logging

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
src/
├── langgraphagenticai/
│   ├── LLMS/         # LLM integration
│   ├── graph/        # Graph builder and configuration
│   ├── nodes/        # Custom nodes for the graph
│   ├── state/        # State management
│   ├── tools/        # Utility functions and tools
│   ├── ui/           # Streamlit UI components
│   └── vectorstore/  # Vector store implementations
├── __init__.py
└── main.py
```

## Dependencies

- langchain
- langgraph
- langchain-community
- langchain-core
- langchain-groq
- langchain-openai
- faiss-cpu
- streamlit

## License

This project is licensed under the Apache 2.0 License.