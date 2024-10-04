# api_validator.py

import logging

def validate_api_key(client):
    """
    Validates the OpenAI API key by making a simple API call.
    """
    try:
        logging.info("Validating OpenAI API key...")
        # Make a simple API call to list available models
        client.models.list()
        logging.info("OpenAI API key is valid.")
    except Exception as e:
        logging.exception("An error occurred while validating the OpenAI API key.")
        raise