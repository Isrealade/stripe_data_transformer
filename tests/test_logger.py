"""Tests for logger utility module."""
import pytest
import logging
import sys
from pathlib import Path
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stripe_data_transformer.utils.logger import get_logger


class TestGetLogger:
    """Test cases for get_logger function."""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a logger instance."""
        logger = get_logger("test_logger")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"

    def test_get_logger_info_level_default(self):
        """Test that logger defaults to INFO level."""
        logger = get_logger("test_logger_info")
        
        assert logger.level == logging.INFO

    def test_get_logger_debug_level(self):
        """Test that logger sets DEBUG level when debug=True."""
        logger = get_logger("test_logger_debug", debug=True)
        
        assert logger.level == logging.DEBUG

    def test_get_logger_has_console_handler(self):
        """Test that logger has a console handler."""
        logger = get_logger("test_logger_handler")
        
        assert len(logger.handlers) > 0
        assert any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers)

    def test_get_logger_handler_level_matches_logger(self):
        """Test that handler level matches logger level."""
        logger = get_logger("test_logger_handler_level", debug=True)
        
        console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(console_handlers) > 0
        assert console_handlers[0].level == logging.DEBUG

    def test_get_logger_formatter(self):
        """Test that logger has a formatter."""
        logger = get_logger("test_logger_formatter")
        
        console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(console_handlers) > 0
        assert console_handlers[0].formatter is not None

    def test_get_logger_clears_old_handlers(self):
        """Test that old handlers are cleared when logger is retrieved again."""
        logger1 = get_logger("test_logger_clear")
        initial_handler_count = len(logger1.handlers)
        
        logger2 = get_logger("test_logger_clear")
        
        # Should have same number of handlers (cleared and re-added)
        assert len(logger2.handlers) == initial_handler_count

    def test_get_logger_different_names(self):
        """Test that different logger names create separate loggers."""
        logger1 = get_logger("logger_one")
        logger2 = get_logger("logger_two")
        
        assert logger1.name != logger2.name
        assert logger1 is not logger2

    def test_get_logger_same_name_returns_same_logger(self):
        """Test that same name returns same logger instance."""
        logger1 = get_logger("same_logger")
        logger2 = get_logger("same_logger")
        
        # Loggers with same name should be the same instance
        assert logger1 is logger2

    def test_get_logger_logging_functionality(self, caplog):
        """Test that logger actually logs messages."""
        logger = get_logger("test_logging", debug=True)
        
        with caplog.at_level(logging.INFO):
            logger.info("Test message")
        
        assert "Test message" in caplog.text

