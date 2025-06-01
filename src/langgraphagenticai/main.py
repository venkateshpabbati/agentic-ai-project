import streamlit as st
import json
from typing import Optional, Dict, Any
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit
from src.langgraphagenticai.state.logger import Logger
from src.langgraphagenticai.security.security_manager import SecurityManager
from typing import TypeVar

T = TypeVar('T')

class SecurityError(Exception):
    """Custom exception for security-related errors."""
    pass

logger = Logger()

def load_langgraph_agenticai_app():
    """
    Main entry point for LangGraph AgenticAI Assistant.
    
    This function orchestrates the entire application workflow with security and privacy considerations:
    1. Initializes the Streamlit UI for user interaction
    2. Processes user input and messages with sanitization
    3. Configures and initializes the LLM model with security checks
    4. Sets up and executes graph-based agent workflows with monitoring
    5. Displays results and handles responses with privacy controls
    
    Security Features:
    - Input validation and sanitization
    - Rate limiting
    - Session management
    - Error handling with privacy considerations
    - Logging with PII masking
    
    Returns:
        None
    
    Raises:
        ValueError: If there's a critical failure in application execution
        SecurityError: If security checks fail
    """
    try:
        # Initialize security manager
        security_manager = SecurityManager()
        
        # Initialize session
        if not security_manager.initialize_session():
            raise SecurityError("Failed to initialize session")
        
        # Check rate limiting
        if not security_manager.check_rate_limit():
            raise SecurityError("Rate limit exceeded")

        # Initialize UI components
        ui = LoadStreamlitUI()
        
        # Load initial UI configuration
        user_input = ui.load_streamlit_ui()
        if not user_input:
            raise ValueError("Failed to load UI configuration")

        # Initialize chat input
        user_message = None
        if st.session_state.IsFetchButtonClicked:
            user_message = st.session_state.timeframe
        else:
            user_message = st.chat_input("Enter your message:")

        if user_message:
            # Validate and sanitize input
            sanitized_message = security_manager.validate_input(user_message)
            if not sanitized_message:
                raise SecurityError("Invalid input detected")

            try:
                # Configure LLM
                llm_config = GroqLLM(user_controls_input=user_input)
                model = llm_config.get_llm_model()
                
                if not model:
                    raise ValueError("Failed to initialize LLM model")

                # Get selected use case
                usecase = user_input.get('selected_usecase')
                if not usecase:
                    raise ValueError("No use case selected")

                # Build and execute graph
                graph_builder = GraphBuilder(model)
                try:
                    graph = graph_builder.setup_graph(usecase)
                    if not graph:
                        raise ValueError("Failed to build graph")

                    # Display results
                    result_display = DisplayResultStreamlit(usecase, graph, sanitized_message)
                    result_display.display_result_on_ui()
                    logger.info(f"Successfully processed message: {sanitized_message}")

                except Exception as graph_error:
                    logger.error(f"Graph setup failed: {str(graph_error)}")
                    raise ValueError(f"Graph setup failed: {str(graph_error)}")

            except Exception as llm_error:
                logger.error(f"LLM processing failed: {str(llm_error)}")
                raise ValueError(f"LLM processing failed: {str(llm_error)}")

    except SecurityError as se:
        st.error(f"Security Error: {str(se)}")
        logger.error(f"Security violation: {str(se)}")
        return
    
    except Exception as e:
        st.error(f"Critical Error: Application failed - {str(e)}")
        logger.critical(f"Application failed: {str(e)}")
        raise ValueError(f"Application failed with exception: {str(e)}")

if __name__ == "__main__":
    try:
        load_langgraph_agenticai_app()
    except Exception as e:
        logger.critical(f"Application startup failed: {str(e)}")
        st.error(f"Application startup failed: {str(e)}")
