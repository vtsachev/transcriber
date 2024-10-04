# main.py

import sys
import os
import logging
import argparse
from openai import OpenAI

from logger_config import configure_logging
from api_validator import validate_api_key
from app import TranscriberApp

def main():
    try:
        # Configure logging
        configure_logging()

        # Parse command-line arguments
        parser = argparse.ArgumentParser(description='Transcribe and process audio files.')
        parser.add_argument('input_file', help='Path to the audio file or transcript file.')
        parser.add_argument('--transcript', action='store_true', help='Indicates that the input file is a transcript.')
        args = parser.parse_args()

        input_file_path = args.input_file
        if not os.path.exists(input_file_path):
            logging.error(f"Input file not found at '{input_file_path}'")
            sys.exit(1)

        # Load your API key from an environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logging.error("OPENAI_API_KEY environment variable not set.")
            sys.exit(1)

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        # Validate the OpenAI API key
        try:
            validate_api_key(client)
        except Exception:
            logging.exception("Failed to validate OpenAI API key.")
            sys.exit(1)

        # Initialize and run the application
        app = TranscriberApp(client)
        app.run(input_file_path, args.transcript)

        logging.info("Processing completed successfully.")

    except Exception:
        logging.exception("An unexpected error occurred in the main function.")
        sys.exit(1)

if __name__ == "__main__":
    main()