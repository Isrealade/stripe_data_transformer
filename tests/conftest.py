"""Shared pytest fixtures for all tests."""
import pytest
import os
from unittest.mock import Mock, MagicMock
from datetime import datetime


@pytest.fixture
def mock_stripe_api_key():
    """Mock Stripe API key for testing."""
    return "sk_test_1234567890abcdef"


@pytest.fixture
def sample_stripe_charge():
    """Sample Stripe charge data."""
    return {
        "id": "ch_1234567890",
        "amount": 2000,  # $20.00 in cents
        "currency": "usd",
        "created": 1609459200,  # Unix timestamp
        "status": "succeeded",
        "payment_method": "pm_1234567890",
        "payment_method_details": {
            "card": {
                "brand": "visa",
                "last4": "4242"
            }
        }
    }


@pytest.fixture
def sample_stripe_charges_list(sample_stripe_charge):
    """List of sample Stripe charges."""
    charges = []
    for i in range(3):
        charge = sample_stripe_charge.copy()
        charge["id"] = f"ch_{i}"
        charge["amount"] = (i + 1) * 1000
        charge["created"] = 1609459200 + (i * 86400)
        charges.append(charge)
    return charges


@pytest.fixture
def mock_stripe_api_response_single_page(sample_stripe_charges_list):
    """Mock Stripe API response with single page (no pagination)."""
    return {
        "object": "list",
        "data": sample_stripe_charges_list,
        "has_more": False
    }


@pytest.fixture
def mock_stripe_api_response_multiple_pages(sample_stripe_charge):
    """Mock Stripe API response with pagination."""
    page1 = {
        "object": "list",
        "data": [sample_stripe_charge.copy() for _ in range(2)],
        "has_more": True
    }
    page2 = {
        "object": "list",
        "data": [sample_stripe_charge.copy() for _ in range(1)],
        "has_more": False
    }
    return [page1, page2]


@pytest.fixture
def mock_config():
    """Mock config dictionary."""
    return {
        "STRIPE_API_KEY": "sk_test_1234567890abcdef",
        "BASE_URL": "https://api.stripe.com",
        "debug": False
    }


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables."""
    monkeypatch.setenv("STRIPE_API_KEY", "sk_test_1234567890abcdef")
    monkeypatch.setenv("BUCKET_NAME", "test-bucket")
    monkeypatch.setenv("DEBUG", "false")


@pytest.fixture
def mock_s3_client():
    """Mock boto3 S3 client."""
    mock_client = MagicMock()
    mock_client.upload_file = MagicMock(return_value=None)
    return mock_client


@pytest.fixture
def temp_csv_file(tmp_path):
    """Create a temporary CSV file for testing."""
    csv_file = tmp_path / "test_stripe_data.csv"
    csv_file.write_text("Transaction ID,Amount ($),Currency,Date,Status\nch_1,10.00,usd,2021-01-01,Succeeded\n")
    return str(csv_file)


@pytest.fixture(autouse=True)
def reset_fetch_params():
    """Reset fetch_charges params between tests to avoid mutation issues."""
    yield
    # Reset params after each test
    try:
        import stripe_data_transformer.services.fetch_charges as fetch_module
        fetch_module.params = {"limit": 100}
    except (ImportError, AttributeError):
        pass

