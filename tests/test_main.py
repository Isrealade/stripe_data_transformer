"""Tests for main module."""
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stripe_data_transformer.main import run


class TestRun:
    """Test cases for run function."""

    @patch('stripe_data_transformer.main.loader_to_warehouse')
    @patch('stripe_data_transformer.main.data_transformer')
    @patch('stripe_data_transformer.main.fetch_all_charges')
    @patch('stripe_data_transformer.main.config')
    def test_run_success(
        self,
        mock_config,
        mock_fetch_charges,
        mock_data_transformer,
        mock_loader,
        sample_stripe_charges_list
    ):
        """Test successful execution of run function."""
        # Setup mocks
        mock_config.get.return_value = False
        mock_config.__getitem__.return_value = "sk_test_123"
        mock_fetch_charges.return_value = sample_stripe_charges_list
        mock_data_transformer.return_value = "stripe_data.csv"
        mock_loader.return_value = True

        # Execute
        run()

        # Assertions
        mock_fetch_charges.assert_called_once_with("sk_test_123")
        mock_data_transformer.assert_called_once_with(sample_stripe_charges_list)
        mock_loader.assert_called_once_with("stripe_data.csv")

    @patch('stripe_data_transformer.main.loader_to_warehouse')
    @patch('stripe_data_transformer.main.data_transformer')
    @patch('stripe_data_transformer.main.fetch_all_charges')
    @patch('stripe_data_transformer.main.config')
    @patch('stripe_data_transformer.main.logging')
    def test_run_fetch_charges_exception(
        self,
        mock_logging,
        mock_config,
        mock_fetch_charges,
        mock_data_transformer,
        mock_loader
    ):
        """Test handling of exception in fetch_all_charges."""
        # Setup mocks
        mock_config.get.return_value = False
        mock_config.__getitem__.return_value = "sk_test_123"
        mock_fetch_charges.side_effect = Exception("API Error")

        # Execute
        run()

        # Assertions
        mock_fetch_charges.assert_called_once()
        mock_data_transformer.assert_not_called()
        mock_loader.assert_not_called()
        mock_logging.exception.assert_called_once()

    @patch('stripe_data_transformer.main.loader_to_warehouse')
    @patch('stripe_data_transformer.main.data_transformer')
    @patch('stripe_data_transformer.main.fetch_all_charges')
    @patch('stripe_data_transformer.main.config')
    @patch('stripe_data_transformer.main.logging')
    def test_run_data_transformer_exception(
        self,
        mock_logging,
        mock_config,
        mock_fetch_charges,
        mock_data_transformer,
        mock_loader,
        sample_stripe_charges_list
    ):
        """Test handling of exception in data_transformer."""
        # Setup mocks
        mock_config.get.return_value = False
        mock_config.__getitem__.return_value = "sk_test_123"
        mock_fetch_charges.return_value = sample_stripe_charges_list
        mock_data_transformer.side_effect = Exception("Transform Error")

        # Execute
        run()

        # Assertions
        mock_fetch_charges.assert_called_once()
        mock_data_transformer.assert_called_once()
        mock_loader.assert_not_called()
        mock_logging.exception.assert_called_once()

    @patch('stripe_data_transformer.main.loader_to_warehouse')
    @patch('stripe_data_transformer.main.data_transformer')
    @patch('stripe_data_transformer.main.fetch_all_charges')
    @patch('stripe_data_transformer.main.config')
    @patch('stripe_data_transformer.main.logging')
    def test_run_loader_exception(
        self,
        mock_logging,
        mock_config,
        mock_fetch_charges,
        mock_data_transformer,
        mock_loader,
        sample_stripe_charges_list
    ):
        """Test handling of exception in loader_to_warehouse."""
        # Setup mocks
        mock_config.get.return_value = False
        mock_config.__getitem__.return_value = "sk_test_123"
        mock_fetch_charges.return_value = sample_stripe_charges_list
        mock_data_transformer.return_value = "stripe_data.csv"
        mock_loader.side_effect = Exception("Loader Error")

        # Execute
        run()

        # Assertions
        mock_fetch_charges.assert_called_once()
        mock_data_transformer.assert_called_once()
        mock_loader.assert_called_once()
        mock_logging.exception.assert_called_once()

    @patch('stripe_data_transformer.main.loader_to_warehouse')
    @patch('stripe_data_transformer.main.data_transformer')
    @patch('stripe_data_transformer.main.fetch_all_charges')
    @patch('stripe_data_transformer.main.config')
    def test_run_empty_charges_list(
        self,
        mock_config,
        mock_fetch_charges,
        mock_data_transformer,
        mock_loader
    ):
        """Test run with empty charges list."""
        # Setup mocks
        mock_config.get.return_value = False
        mock_config.__getitem__.return_value = "sk_test_123"
        mock_fetch_charges.return_value = []
        mock_data_transformer.return_value = "stripe_data.csv"
        mock_loader.return_value = True

        # Execute
        run()

        # Assertions - should still complete successfully
        mock_fetch_charges.assert_called_once()
        mock_data_transformer.assert_called_once_with([])
        mock_loader.assert_called_once()

