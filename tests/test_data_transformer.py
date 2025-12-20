"""Tests for data_transformer module."""
import pytest
import pandas as pd
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stripe_data_transformer.services.data_transformer import data_transformer


class TestDataTransformer:
    """Test cases for data_transformer function."""

    def test_data_transformer_basic_transformation(self, sample_stripe_charges_list, tmp_path):
        """Test basic data transformation from JSON to CSV."""
        # Change to temp directory
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            result = data_transformer(sample_stripe_charges_list)
            
            # Check that CSV file was created
            assert os.path.exists(result)
            assert result == "stripe_data.csv"
            
            # Read CSV and verify content
            df = pd.read_csv(result)
            
            # Check columns
            expected_columns = [
                "Transaction ID",
                "Amount ($)",
                "Currency",
                "Date",
                "Status",
                "Payment Method ID",
                "Card Brand",
                "Last 4 Digits"
            ]
            assert all(col in df.columns for col in expected_columns)
            
            # Check data
            assert len(df) == 3
            assert df["Transaction ID"].iloc[0] == "ch_0"
            
        finally:
            os.chdir(original_dir)
            # Cleanup
            if os.path.exists("stripe_data.csv"):
                os.remove("stripe_data.csv")

    def test_data_transformer_amount_conversion(self, sample_stripe_charges_list, tmp_path):
        """Test that amounts are converted from cents to dollars."""
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            result = data_transformer(sample_stripe_charges_list)
            df = pd.read_csv(result)
            
            # Check amount conversion (2000 cents = $20.00)
            assert df["Amount ($)"].iloc[0] == 10.00  # First charge is 1000 cents = $10
            assert df["Amount ($)"].iloc[1] == 20.00  # Second charge is 2000 cents = $20
            
        finally:
            os.chdir(original_dir)
            if os.path.exists("stripe_data.csv"):
                os.remove("stripe_data.csv")

    def test_data_transformer_date_conversion(self, sample_stripe_charges_list, tmp_path):
        """Test that Unix timestamps are converted to datetime."""
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            result = data_transformer(sample_stripe_charges_list)
            df = pd.read_csv(result, parse_dates=["Date"])
            
            # Check date conversion (CSV stores as string, so we parse it)
            assert pd.api.types.is_datetime64_any_dtype(df["Date"])
            # Verify the date is reasonable (not NaT)
            assert not df["Date"].isna().any()
            # Verify dates are in expected range (after 2020)
            assert df["Date"].min().year >= 2020
            
        finally:
            os.chdir(original_dir)
            if os.path.exists("stripe_data.csv"):
                os.remove("stripe_data.csv")

    def test_data_transformer_column_mapping(self, sample_stripe_charges_list, tmp_path):
        """Test that columns are correctly renamed."""
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            result = data_transformer(sample_stripe_charges_list)
            df = pd.read_csv(result)
            
            # Check that original column names are not present
            assert "id" not in df.columns
            assert "amount" not in df.columns
            assert "created" not in df.columns
            
            # Check that new column names are present
            assert "Transaction ID" in df.columns
            assert "Amount ($)" in df.columns
            assert "Date" in df.columns
            
        finally:
            os.chdir(original_dir)
            if os.path.exists("stripe_data.csv"):
                os.remove("stripe_data.csv")

    def test_data_transformer_empty_list(self, tmp_path):
        """Test transformation with empty charge list."""
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            result = data_transformer([])
            df = pd.read_csv(result)
            
            # Should create CSV with headers but no data rows
            assert os.path.exists(result)
            assert len(df) == 0
            # Should have the expected column headers
            expected_columns = [
                "Transaction ID",
                "Amount ($)",
                "Currency",
                "Date",
                "Status",
                "Payment Method ID",
                "Card Brand",
                "Last 4 Digits"
            ]
            assert all(col in df.columns for col in expected_columns)
            
        finally:
            os.chdir(original_dir)
            if os.path.exists("stripe_data.csv"):
                os.remove("stripe_data.csv")

    def test_data_transformer_nested_data(self, tmp_path):
        """Test that nested JSON data is properly flattened."""
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        # Create charge with nested payment_method_details matching the column_map structure
        charge_with_nested = {
            "id": "ch_nested",
            "amount": 5000,
            "currency": "usd",
            "created": 1609459200,
            "status": "succeeded",
            "payment_method": "pm_123",
            "payment_method_details": {
                "card": {
                    "brand": "mastercard",
                    "last4": "1234"
                }
            }
        }
        
        try:
            result = data_transformer([charge_with_nested])
            df = pd.read_csv(result)
            
            # Check that nested fields are accessible (after json_normalize with sep="_")
            # The column names should be payment_method_details_card_brand and payment_method_details_card_last4
            # which get mapped to "Card Brand" and "Last 4 Digits"
            assert "Card Brand" in df.columns
            assert "Last 4 Digits" in df.columns
            # Check values (they might be strings after CSV round-trip)
            assert str(df["Card Brand"].iloc[0]).lower() == "mastercard"
            assert str(df["Last 4 Digits"].iloc[0]) == "1234"
            
        finally:
            os.chdir(original_dir)
            if os.path.exists("stripe_data.csv"):
                os.remove("stripe_data.csv")

    def test_data_transformer_returns_filename(self, sample_stripe_charges_list, tmp_path):
        """Test that function returns the correct filename."""
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            result = data_transformer(sample_stripe_charges_list)
            
            assert isinstance(result, str)
            assert result == "stripe_data.csv"
            
        finally:
            os.chdir(original_dir)
            if os.path.exists("stripe_data.csv"):
                os.remove("stripe_data.csv")

