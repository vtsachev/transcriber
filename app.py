# app.py

import os
import logging

from file_manager import (
    create_tmp_directory,
    create_transcripts_directory,
    create_raw_transcripts_directory,
    get_unique_filename,
)
from audio_splitter import split_audio
from audio_transcriber import transcribe_audio_files
from transcript_processor import process_transcript

class TranscriberApp:
    def __init__(self, client):
        self.client = client
        self.tmp_dir = create_tmp_directory()
        self.transcripts_dir = create_transcripts_directory()
        self.raw_transcripts_dir = create_raw_transcripts_directory()
        logging.info(f"Temporary files will be stored in '{self.tmp_dir}'")
        logging.info(f"Transcripts will be saved in '{self.transcripts_dir}'")
        logging.info(f"Raw transcripts will be saved in '{self.raw_transcripts_dir}'")

    def process_transcript_file(self, transcript_path):
        logging.info(f"Transcript file path: '{transcript_path}'")

        # Read the transcript
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                combined_transcript = f.read()
            logging.info(f"Using provided transcript from '{transcript_path}'")
        except Exception:
            logging.exception(f"Failed to read transcript file '{transcript_path}'.")
            return

        # Prepare the base output file name
        base_name = os.path.splitext(os.path.basename(transcript_path))[0]

        # Determine the unique output file name
        output_filename = get_unique_filename(base_name, ".txt", self.transcripts_dir)
        output_file_path = os.path.join(self.transcripts_dir, output_filename)

        # Process the transcript with GPT-4o-mini
        try:
            process_transcript(self.client, combined_transcript, output_file_path)
        except Exception:
            logging.exception("Failed to process transcript with GPT-4o-mini.")
            return

        logging.info(f"Final transcript saved to '{output_file_path}'")

    def process_audio_file(self, audio_file_path):
        logging.info(f"Audio file path: '{audio_file_path}'")

        # Prepare the base output file name
        base_name = os.path.splitext(os.path.basename(audio_file_path))[0]

        # Split the audio file if necessary
        try:
            audio_chunks = split_audio(audio_file_path, self.tmp_dir)
        except Exception:
            logging.exception("Failed to split audio file.")
            return

        # Transcribe audio files
        try:
            combined_transcript = transcribe_audio_files(self.client, audio_chunks, self.tmp_dir)
        except Exception:
            logging.exception("Failed to transcribe audio files.")
            return

        # Save the combined raw transcript in raw_transcripts directory
        raw_transcript_filename = get_unique_filename(base_name, ".txt", self.raw_transcripts_dir)
        raw_transcript_path = os.path.join(self.raw_transcripts_dir, raw_transcript_filename)
        try:
            with open(raw_transcript_path, "w", encoding="utf-8") as f:
                f.write(combined_transcript)
            logging.info(f"Combined raw transcript saved to '{raw_transcript_path}'")
        except Exception:
            logging.exception(f"Failed to save combined raw transcript to '{raw_transcript_path}'.")
            return

        # Determine the unique output file name for processed transcript
        output_filename = get_unique_filename(base_name, ".txt", self.transcripts_dir)
        output_file_path = os.path.join(self.transcripts_dir, output_filename)

        # Process the transcript with GPT-4o-mini
        try:
            process_transcript(self.client, combined_transcript, output_file_path)
        except Exception:
            logging.exception("Failed to process transcript with GPT-4o-mini.")
            return

        logging.info(f"Final transcript saved to '{output_file_path}'")

    def run(self, input_file_path, is_transcript):
        if is_transcript:
            self.process_transcript_file(input_file_path)
        else:
            self.process_audio_file(input_file_path)