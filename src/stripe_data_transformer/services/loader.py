import logging
from pathlib import Path
from utils.logger import get_logger
from config import config
import os
import boto3
from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError

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
        except (ClientError, S3UploadFailedError) as e:
            logger.error(e)
            return False
        
        logger.info(f"{filepath} loaded successfully to {bucket_name}!")
    
    return True