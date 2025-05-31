import re
import time
from datetime import datetime, timedelta
from typing import Optional
import streamlit as st
from ..state.logger import Logger

logger = Logger()

class SecurityManager:
    """
    Security manager for LangGraph AgenticAI Assistant.
    Handles all security-related operations including:
    - Input validation
    - Rate limiting
    - Session management
    - Security monitoring
    """
    
    def __init__(self):
        self.rate_limit_window = 60  # 1 minute
        self.max_requests = 100
        self.session_timeout = timedelta(minutes=30)
        
    def validate_input(self, user_input: str) -> Optional[str]:
        """
        Validate and sanitize user input.
        
        Args:
            user_input: User input string
            
        Returns:
            Sanitized input or None if invalid
        """
        try:
            # Basic input validation
            if not isinstance(user_input, str):
                return None
                
            # Remove potential XSS/SQL injection patterns
            sanitized = re.sub(r'[<>"\']', '', user_input)
            
            # Check for suspicious patterns
            if any(pattern in sanitized.lower() for pattern in ['drop', 'delete', 'select', 'update']):
                logger.warning(f"Suspicious input detected: {sanitized}")
                return None
                
            return sanitized
            
        except Exception as e:
            logger.error(f"Input validation failed: {str(e)}")
            return None

    def check_rate_limit(self) -> bool:
        """
        Check if rate limit has been exceeded.
        
        Returns:
            True if within limits, False otherwise
        """
        if 'request_count' not in st.session_state:
            st.session_state.request_count = 1
            st.session_state.last_request_time = datetime.now()
            return True
            
        current_time = datetime.now()
        time_diff = current_time - st.session_state.last_request_time
        
        if time_diff.total_seconds() > self.rate_limit_window:
            st.session_state.request_count = 1
            st.session_state.last_request_time = current_time
            return True
            
        if st.session_state.request_count >= self.max_requests:
            logger.warning("Rate limit exceeded")
            return False
            
        st.session_state.request_count += 1
        return True

    def initialize_session(self) -> bool:
        """
        Initialize secure session.
        
        Returns:
            True if session initialized successfully
        """
        try:
            if not hasattr(st.session_state, 'initialized'):
                st.session_state.initialized = True
                st.session_state.session_start = datetime.now()
                st.session_state.last_activity = datetime.now()
                
            # Check session timeout
            if datetime.now() - st.session_state.last_activity > self.session_timeout:
                logger.info("Session timed out")
                self._clear_session()
                return False
                
            st.session_state.last_activity = datetime.now()
            return True
            
        except Exception as e:
            logger.error(f"Session initialization failed: {str(e)}")
            return False

    def _clear_session(self) -> None:
        """
        Clear all session data.
        """
        for key in st.session_state.keys():
            del st.session_state[key]

    def mask_pii(self, text: str) -> str:
        """
        Mask potential PII in text.
        
        Args:
            text: Input text
            
        Returns:
            Text with PII masked
        """
        # Basic PII patterns
        patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{16}\b',  # Credit card
            r'\b\d{10}\b'   # Phone number
        ]
        
        masked_text = text
        for pattern in patterns:
            masked_text = re.sub(pattern, '[REDACTED]', masked_text)
        
        return masked_text

    def log_secure(self, message: str, level: str = 'info') -> None:
        """
        Secure logging with PII masking.
        
        Args:
            message: Message to log
            level: Logging level (info, error, warning)
        """
        masked_message = self.mask_pii(message)
        if level == 'error':
            logger.error(masked_message)
        elif level == 'warning':
            logger.warning(masked_message)
        else:
            logger.info(masked_message)
