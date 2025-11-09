import requests 
import logging
from utils.logger import get_logger
import os
import json
from config import config

logger = get_logger("main", debug=config.get("debug"))

if config.get("debug"):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

params = {
    "limit": 100
}

def fetch_all_charges(stripe_api_key: str) -> list:
    """Function to fetch charges through a get request to Stripe charges endpoint

    Args:
        stripe_api_key (str): api key for stripe account

    Returns:
        list: A JSON list of charges 
    """
     
    url = f"{config['BASE_URL']}/v1/charges"
    charges = []
    starting_after = None
    has_more = True
    
    logger.info("Starting to fetch Stripe charges...")
    
    while has_more:
        try:
            if starting_after:
                params["starting_after"] = starting_after
                
            request = requests.get(
                url,
                params=params,
                headers={
                    "Authorization": f"Bearer {stripe_api_key}"
                    },
                timeout=20
            )
            
            request.raise_for_status()
            
            data = request.json()
            charges.extend(data["data"])
            
            has_more = data["has_more"]
            
            logger.info("Fetched %d charges, has_more=%s", len(data["data"]), has_more)
             
            if has_more:
                logger.info("Fetching more charges....")
                starting_after = data["data"][-1]["id"]
 
            
        except requests.exceptions.JSONDecodeError as e:
            logging.error(f"Couldn't decode into json: {e}")
            
        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error while fetching charges after ID %s: %s", starting_after, e)
            
        except requests.exceptions.Timeout as e:
            logging.error(f"The request timed out: {e}")
            print(f"The request timed out: {e}")
            
        except Exception:
            logger.exception("Unexpected error while fetching charges")
    
    return charges