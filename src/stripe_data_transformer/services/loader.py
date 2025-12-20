import logging
from pathlib import Path
from stripe_data_transformer.utils.logger import get_logger
from stripe_data_transformer.config import config
import os
import boto3
from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import (NoCredentialsError, PartialCredentialsError, ClientError)

logger = get_logger("main", debug=config.get("debug"))

def loader_to_warehouse(filepath: Path) -> bool:
    bucket_name = os.getenv("BUCKET_NAME")
    if bucket_name:
        s3 = boto3.client('s3')
        logger.info(f"uploading {filepath} into {bucket_name}....")
        
        try:
            _response = s3.upload_file(
                filepath, 
                Bucket=bucket_name,
                Key=filepath
            )
        except NoCredentialsError as e:
            logger.error(f"No AWS credentials found: {e}")
            print("No AWS credentials found.")
            return False

        except PartialCredentialsError as e:
            logger.error(f"Incomplete AWS credentials: {e}")
            print("Incomplete credentials.")
            return False

        except ClientError as e:
            code = e.response["Error"]["Code"]
            message = e.response["Error"].get("Message", "")

            if code == "NoSuchBucket":
                logger.error(f"S3 Error - NoSuchBucket: {message}")
                print("Bucket doesn't exist.")
                return False

            elif code == "NoSuchKey":
                logger.error(f"S3 Error - NoSuchKey: {message}")
                print("File doesn't exist.")
                return False

            elif code == "AccessDenied":
                logger.error(f"S3 Error - AccessDenied: {message}")
                print("Permission denied.")
                return False

            else:
                logger.error(f"Unhandled AWS ClientError [{code}]: {message}")
                print(f"Unhandled AWS error: {code}")
                return False

        except Exception as e:
            # Catch-all for unexpected issues
            logger.error(f"Unexpected error: {e}")
            print("An unexpected error occurred.")
            return False
        
        logger.info(f"{filepath} loaded successfully to {bucket_name}!")
    
    return True