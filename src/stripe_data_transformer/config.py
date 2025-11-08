import os 
from dotenv import load_dotenv
from typing import Any


load_dotenv()

column_map = {
    "id": "Transaction ID",
    "amount": "Amount ($)",
    "currency": "Currency",
    "created": "Date",
    "status": "Status",
    "payment_method": "Payment Method ID",
    "payment_method_details_card_brand": "Card Brand",
    "payment_method_details_card_last4": "Last 4 Digits"
}

def str_to_bool(value: str) -> bool:
    return value.lower() in ("1", "true", "yes", "on")

config: dict[str, Any] = {
    "STRIPE_API_KEY": os.environ["STRIPE_API_KEY"],
    "BASE_URL": "https://api.stripe.com",
    "debug": str_to_bool(os.getenv("DEBUG", "false"))
}