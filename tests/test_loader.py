"""Tests for loader module."""
import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stripe_data_transformer.services.loader import loader_to_warehouse


class TestLoaderToWarehouse:
    """Test cases for loader_to_warehouse function."""

    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    @patch('stripe_data_transformer.services.loader.boto3.client')
    def test_loader_to_warehouse_success(
        self,
        mock_boto3_client,
        temp_csv_file
    ):
        """Test successful S3 upload."""
        mock_s3_client = MagicMock()
        mock_s3_client.upload_file = MagicMock(return_value=None)
        mock_boto3_client.return_value = mock_s3_client

        result = loader_to_warehouse(temp_csv_file)

        assert result is True
        mock_s3_client.upload_file.assert_called_once_with(
            temp_csv_file,
            Bucket="test-bucket",
            Key=temp_csv_file
        )

    @patch.dict(os.environ, {"BUCKET_NAME": ""}, clear=False)
    def test_loader_to_warehouse_no_bucket_name(self, temp_csv_file):
        """Test that function returns True when BUCKET_NAME is not set."""
        result = loader_to_warehouse(temp_csv_file)
        assert result is True

    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    @patch('stripe_data_transformer.services.loader.boto3.client')
    def test_loader_to_warehouse_no_credentials(
        self,
        mock_boto3_client,
        temp_csv_file
    ):
        """Test handling of missing AWS credentials."""
        mock_s3_client = MagicMock()
        mock_s3_client.upload_file.side_effect = NoCredentialsError()
        mock_boto3_client.return_value = mock_s3_client

        result = loader_to_warehouse(temp_csv_file)

        assert result is False
        mock_s3_client.upload_file.assert_called_once()

    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    @patch('stripe_data_transformer.services.loader.boto3.client')
    def test_loader_to_warehouse_partial_credentials(
        self,
        mock_boto3_client,
        temp_csv_file
    ):
        """Test handling of incomplete AWS credentials."""
        mock_s3_client = MagicMock()
        mock_s3_client.upload_file.side_effect = PartialCredentialsError(
            provider='test',
            cred_var='test_var'
        )
        mock_boto3_client.return_value = mock_s3_client

        result = loader_to_warehouse(temp_csv_file)

        assert result is False

    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    @patch('stripe_data_transformer.services.loader.boto3.client')
    def test_loader_to_warehouse_bucket_not_found(
        self,
        mock_boto3_client,
        temp_csv_file
    ):
        """Test handling of non-existent bucket."""
        mock_s3_client = MagicMock()
        error_response = {
            "Error": {
                "Code": "NoSuchBucket",
                "Message": "The specified bucket does not exist"
            }
        }
        mock_s3_client.upload_file.side_effect = ClientError(error_response, "PutObject")
        mock_boto3_client.return_value = mock_s3_client

        result = loader_to_warehouse(temp_csv_file)

        assert result is False

    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    @patch('stripe_data_transformer.services.loader.boto3.client')
    def test_loader_to_warehouse_access_denied(
        self,
        mock_boto3_client,
        temp_csv_file
    ):
        """Test handling of access denied error."""
        mock_s3_client = MagicMock()
        error_response = {
            "Error": {
                "Code": "AccessDenied",
                "Message": "Access Denied"
            }
        }
        mock_s3_client.upload_file.side_effect = ClientError(error_response, "PutObject")
        mock_boto3_client.return_value = mock_s3_client

        result = loader_to_warehouse(temp_csv_file)

        assert result is False

    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    @patch('stripe_data_transformer.services.loader.boto3.client')
    def test_loader_to_warehouse_other_client_error(
        self,
        mock_boto3_client,
        temp_csv_file
    ):
        """Test handling of other ClientError types."""
        mock_s3_client = MagicMock()
        error_response = {
            "Error": {
                "Code": "InvalidRequest",
                "Message": "Invalid request"
            }
        }
        mock_s3_client.upload_file.side_effect = ClientError(error_response, "PutObject")
        mock_boto3_client.return_value = mock_s3_client

        result = loader_to_warehouse(temp_csv_file)

        assert result is False

    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    @patch('stripe_data_transformer.services.loader.boto3.client')
    def test_loader_to_warehouse_unexpected_error(
        self,
        mock_boto3_client,
        temp_csv_file
    ):
        """Test handling of unexpected errors."""
        mock_s3_client = MagicMock()
        mock_s3_client.upload_file.side_effect = Exception("Unexpected error")
        mock_boto3_client.return_value = mock_s3_client

        result = loader_to_warehouse(temp_csv_file)

        assert result is False

    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    @patch('stripe_data_transformer.services.loader.boto3.client')
    def test_loader_to_warehouse_correct_parameters(
        self,
        mock_boto3_client,
        temp_csv_file
    ):
        """Test that upload_file is called with correct parameters."""
        mock_s3_client = MagicMock()
        mock_s3_client.upload_file = MagicMock(return_value=None)
        mock_boto3_client.return_value = mock_s3_client

        loader_to_warehouse(temp_csv_file)

        mock_s3_client.upload_file.assert_called_once()
        call_args = mock_s3_client.upload_file.call_args
        assert call_args[0][0] == temp_csv_file  # filepath
        assert call_args[1]["Bucket"] == "test-bucket"
        assert call_args[1]["Key"] == temp_csv_file

