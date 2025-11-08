import logging
from utils.logger import get_logger
from stripe_data_transformer.services.fetch_charges import fetch_all_charges
from stripe_data_transformer.services.data_transformer import data_transformer
from stripe_data_transformer.services.loader import loader_to_warehouse
from config import config


logger = get_logger("main", debug=config.get("debug"))

def run():
    """_summary_
    """
    try:
        charges = fetch_all_charges(config["STRIPE_API_KEY"])
        file = data_transformer(charges)
        loader_to_warehouse(file)
        
    except Exception as e:
        logging.exception(e)
        
    


if __name__ == "__main__":
    run()