import streamlit as st
import json
from typing import Optional, Dict, Any
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit
from src.langgraphagenticai.state.logger import Logger

logger = Logger()

def load_langgraph_agenticai_app():
    """
    Main entry point for LangGraph AgenticAI Assistant.
    
    This function orchestrates the entire application workflow:
    1. Initializes the Streamlit UI for user interaction
    2. Processes user input and messages
    3. Configures and initializes the LLM model
    4. Sets up and executes graph-based agent workflows
    5. Displays results and handles responses
    
    Returns:
        None
    
    Raises:
        ValueError: If there's a critical failure in application execution
    """
    try:
        # Initialize UI components
        ui = LoadStreamlitUI()
        
        # Load initial UI configuration
        user_input = ui.load_streamlit_ui()
        if not user_input:
            st.error("Error: Failed to load UI configuration")
            logger.error("Failed to load UI configuration")
            return

        # Initialize chat input
        user_message = None
        if st.session_state.IsFetchButtonClicked:
            user_message = st.session_state.timeframe
        else:
            user_message = st.chat_input("Enter your message:")

        if user_message:
            try:
                # Configure LLM
                llm_config = GroqLLM(user_controls_input=user_input)
                model = llm_config.get_llm_model()
                
                if not model:
                    st.error("Error: Failed to initialize LLM model")
                    logger.error("LLM model initialization failed")
                    return

                # Get selected use case
                usecase = user_input.get('selected_usecase')
                if not usecase:
                    st.error("Error: No use case selected")
                    logger.error("No use case selected")
                    return

                # Build and execute graph
                graph_builder = GraphBuilder(model)
                try:
                    graph = graph_builder.setup_graph(usecase)
                    if not graph:
                        st.error("Error: Failed to build graph")
                        logger.error("Graph setup failed")
                        return

                    # Display results
                    result_display = DisplayResultStreamlit(usecase, graph, user_message)
                    result_display.display_result_on_ui()
                    logger.info(f"Successfully processed message: {user_message}")

                except Exception as graph_error:
                    st.error(f"Error: Graph setup failed - {str(graph_error)}")
                    logger.error(f"Graph setup failed: {str(graph_error)}")
                    return

            except Exception as llm_error:
                st.error(f"Error: LLM processing failed - {str(llm_error)}")
                logger.error(f"LLM processing failed: {str(llm_error)}")
                return

    except Exception as e:
        st.error(f"Critical Error: Application failed - {str(e)}")
        logger.critical(f"Application failed: {str(e)}")
        raise ValueError(f"Application failed with exception: {str(e)}")

if __name__ == "__main__":
    load_langgraph_agenticai_app()
