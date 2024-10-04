# audio_transcriber.py

import os
import logging
from pydub import AudioSegment

SUPPORTED_FORMATS = ('.wav', '.mp3', '.mp4', '.m4a', '.mpeg', '.mpga', '.webm')

def transcribe_audio_files(client, audio_files, tmp_dir):
    """
    Transcribes each audio chunk and returns the combined transcript.

    Parameters:
    - client: OpenAI client object
    - audio_files: List of paths to audio files.
    - tmp_dir: Directory to save any converted audio files.

    Returns:
    - combined_transcript: String containing the combined transcript.
    """
    combined_transcript = ""

    for audio_file_path in sorted(audio_files):
        try:
            logging.info(f"Processing file: '{audio_file_path}'")

            # Check file size
            file_size = os.path.getsize(audio_file_path)
            if file_size > 25 * 1024 * 1024:
                logging.warning(f"File '{audio_file_path}' exceeds 25 MB limit and will be skipped.")
                continue

            # Check if the file is in a supported format
            ext = os.path.splitext(audio_file_path)[1].lower()
            if ext not in SUPPORTED_FORMATS:
                logging.warning(f"File '{audio_file_path}' has an unsupported format '{ext}'. Attempting to convert to WAV.")

                # Convert audio file to 'wav' format
                audio = AudioSegment.from_file(audio_file_path)
                base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
                converted_file_path = os.path.join(tmp_dir, f"{base_name}.wav")
                audio.export(converted_file_path, format='wav')
                audio_file_path = converted_file_path
                logging.info(f"Converted '{audio_file_path}' to WAV format.")

            # Read the audio file
            logging.info("Reading audio file...")
            with open(audio_file_path, "rb") as audio_file:
                logging.info("Transcribing audio file...")
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                logging.info("Transcription completed.")

            # Extract the transcript text
            transcript_text = transcription.text
            if not transcript_text:
                logging.warning(f"Transcription returned empty text for '{audio_file_path}'.")
                continue

            # Append to the combined transcript
            combined_transcript += transcript_text + "\n"

        except Exception as e:
            logging.exception(f"An error occurred while processing '{audio_file_path}'.")
            raise

    return combined_transcript