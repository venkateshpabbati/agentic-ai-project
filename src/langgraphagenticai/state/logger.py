"""
Logging module for the LangGraph AgenticAI application.
"""

import logging
from datetime import datetime
import os
from pathlib import Path

class Logger:
    """
    Custom logger class for the LangGraph AgenticAI application.
    
    Provides structured logging with different levels and file output.
    """
    def __init__(self):
        # Create logs directory if it doesn't exist
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Create log file name with timestamp
        log_file = logs_dir / f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)

    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)

    def critical(self, message: str) -> None:
        """Log a critical error message."""
        self.logger.critical(message)
