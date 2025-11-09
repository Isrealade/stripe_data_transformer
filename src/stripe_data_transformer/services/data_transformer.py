import logging
from utils.logger import get_logger
from config import config, column_map
from pathlib import Path
import pandas as pd

logger = get_logger("main", debug=config.get("debug"))

def data_transformer(charges: list) -> str:
    """A function to transform a list of json data to CSV using Panda library

    Args:
        data (list): A list of JSOn data 

    Returns:
        str: _description_
    """
    logger.info("Transforming Stripe charges into DataFrame...")
    
    df = pd.json_normalize(charges, sep="_") ## Normalize semi-structured JSON data into a dataframe
    
    logger.debug(f"Columns available: {df.columns.tolist()}")
    
    logger.info("Renaming Columns...")
    df = df[list(column_map.keys())].rename(columns=column_map)

    df["Amount ($)"] = df["Amount ($)"] / 100
    df["Date"] = pd.to_datetime(df["Date"], unit="s")

    filename = "stripe_data.csv"
    df.to_csv(filename, index=False)
    
    logger.info(f"Saved CSV to file: {filename}")
    
    return filename
    
    
    
    
    
    
    
    