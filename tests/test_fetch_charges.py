"""Tests for fetch_charges module."""
import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stripe_data_transformer.services.fetch_charges import fetch_all_charges


class TestFetchAllCharges:
    """Test cases for fetch_all_charges function."""

    @patch('stripe_data_transformer.services.fetch_charges.requests.get')
    def test_fetch_all_charges_single_page(
        self, 
        mock_get, 
        mock_stripe_api_key,
        mock_stripe_api_response_single_page
    ):
        """Test fetching charges with single page (no pagination)."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = mock_stripe_api_response_single_page
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Execute
        result = fetch_all_charges(mock_stripe_api_key)

        # Assertions
        assert len(result) == 3
        assert result[0]["id"] == "ch_0"
        mock_get.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

    @patch('stripe_data_transformer.services.fetch_charges.requests.get')
    def test_fetch_all_charges_multiple_pages(
        self,
        mock_get,
        mock_stripe_api_key,
        mock_stripe_api_response_multiple_pages
    ):
        """Test fetching charges with pagination."""
        # Reset params to avoid mutation issues between tests
        import stripe_data_transformer.services.fetch_charges as fetch_module
        fetch_module.params = {"limit": 100}
        
        # Setup mock responses for pagination
        responses = []
        for page_data in mock_stripe_api_response_multiple_pages:
            mock_response = Mock()
            mock_response.json.return_value = page_data
            mock_response.raise_for_status = Mock()
            responses.append(mock_response)
        
        mock_get.side_effect = responses

        # Execute
        result = fetch_all_charges(mock_stripe_api_key)

        # Assertions
        assert len(result) == 3  # 2 from first page + 1 from second page
        assert mock_get.call_count == 2
        
        # Check that starting_after parameter was used in second call
        second_call_kwargs = mock_get.call_args_list[1].kwargs
        assert "starting_after" in second_call_kwargs.get("params", {})

    @patch('stripe_data_transformer.services.fetch_charges.requests.get')
    def test_fetch_all_charges_empty_result(
        self,
        mock_get,
        mock_stripe_api_key
    ):
        """Test fetching when no charges are returned."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "object": "list",
            "data": [],
            "has_more": False
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = fetch_all_charges(mock_stripe_api_key)

        assert result == []
        assert len(result) == 0

    @patch('stripe_data_transformer.services.fetch_charges.requests.get')
    def test_fetch_all_charges_http_error(
        self,
        mock_get,
        mock_stripe_api_key
    ):
        """Test handling of HTTP errors."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Unauthorized")
        mock_get.return_value = mock_response

        result = fetch_all_charges(mock_stripe_api_key)

        # Should return empty list or partial results on error
        assert isinstance(result, list)

    @patch('stripe_data_transformer.services.fetch_charges.requests.get')
    def test_fetch_all_charges_timeout(
        self,
        mock_get,
        mock_stripe_api_key
    ):
        """Test handling of timeout errors."""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        result = fetch_all_charges(mock_stripe_api_key)

        # Should return empty list or partial results on timeout
        assert isinstance(result, list)

    @patch('stripe_data_transformer.services.fetch_charges.requests.get')
    def test_fetch_all_charges_json_decode_error(
        self,
        mock_get,
        mock_stripe_api_key
    ):
        """Test handling of JSON decode errors."""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = fetch_all_charges(mock_stripe_api_key)

        # Should return empty list or partial results on JSON error
        assert isinstance(result, list)

    @patch('stripe_data_transformer.services.fetch_charges.requests.get')
    def test_fetch_all_charges_authorization_header(
        self,
        mock_get,
        mock_stripe_api_key,
        mock_stripe_api_response_single_page
    ):
        """Test that Authorization header is correctly set."""
        mock_response = Mock()
        mock_response.json.return_value = mock_stripe_api_response_single_page
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        fetch_all_charges(mock_stripe_api_key)

        # Check Authorization header
        call_kwargs = mock_get.call_args.kwargs
        assert "headers" in call_kwargs
        assert call_kwargs["headers"]["Authorization"] == f"Bearer {mock_stripe_api_key}"

    @patch('stripe_data_transformer.services.fetch_charges.requests.get')
    def test_fetch_all_charges_params_limit(
        self,
        mock_get,
        mock_stripe_api_key,
        mock_stripe_api_response_single_page
    ):
        """Test that limit parameter is set correctly."""
        mock_response = Mock()
        mock_response.json.return_value = mock_stripe_api_response_single_page
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        fetch_all_charges(mock_stripe_api_key)

        # Check params include limit
        call_kwargs = mock_get.call_args.kwargs
        assert "params" in call_kwargs
        assert call_kwargs["params"]["limit"] == 100

