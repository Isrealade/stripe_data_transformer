import logging
from stripe_data_transformer.utils.logger import get_logger
from stripe_data_transformer.config import config, column_map
from pathlib import Path
import pandas as pd

logger = get_logger("main", debug=config.get("debug"))

def data_transformer(charges: list) -> str:
    """A function to transform a list of json data to CSV using Panda library

    Args:
        charges (list): A list of JSON charge data 

    Returns:
        str: Filename of the created CSV file
    """
    logger.info("Transforming Stripe charges into DataFrame...")
    
    # Handle empty list
    if not charges:
        logger.warning("Empty charges list provided. Creating empty CSV with headers.")
        # Create empty DataFrame with expected columns
        df = pd.DataFrame(columns=list(column_map.keys()))
        df = df.rename(columns=column_map)
    else:
        df = pd.json_normalize(charges, sep="_") ## Normalize semi-structured JSON data into a dataframe
        
        logger.debug(f"Columns available: {df.columns.tolist()}")
        
        logger.info("Renaming Columns...")
        # Only select columns that exist in the DataFrame
        available_columns = [col for col in column_map.keys() if col in df.columns]
        if not available_columns:
            raise ValueError("No expected columns found in the data. Please check the input data structure.")
        
        df = df[available_columns].rename(columns=column_map)
        
        # Convert amount if column exists and DataFrame is not empty
        if "Amount ($)" in df.columns and not df.empty:
            df["Amount ($)"] = df["Amount ($)"] / 100
        
        # Convert date if column exists and DataFrame is not empty
        if "Date" in df.columns and not df.empty:
            df["Date"] = pd.to_datetime(df["Date"], unit="s")

    filename = "stripe_data.csv"
    df.to_csv(filename, index=False)
    
    logger.info(f"Saved CSV to file: {filename}")
    
    return filename
    
    
    
    
    
    
    
    