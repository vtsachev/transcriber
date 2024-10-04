# audio_splitter.py

import os
import logging
from pydub import AudioSegment

def split_audio(file_path, tmp_dir):
    """
    Splits the audio file into chunks less than 25 MB and saves them in the tmp directory.

    Parameters:
    - file_path: Path to the audio file.
    - tmp_dir: Directory to save the split audio chunks.

    Returns:
    - chunks: List of paths to the audio files (original file or split chunks).
    """
    try:
        # Get the file size in bytes
        file_size = os.path.getsize(file_path)
        max_chunk_size_bytes = 25 * 1024 * 1024  # 25 MB
        logging.info(f"Total file size: {file_size / (1024 * 1024):.2f} MB")

        if file_size <= max_chunk_size_bytes:
            logging.info("Audio file is within the size limit; no splitting needed.")
            return [file_path]

        # Load the audio file
        audio = AudioSegment.from_file(file_path)
        total_length_ms = len(audio)
        logging.info(f"Total audio length: {total_length_ms / 60000:.2f} minutes")

        # Estimate size per millisecond
        size_per_ms = file_size / total_length_ms

        # Calculate maximum chunk length to be under 25 MB
        max_chunk_length_ms = int(max_chunk_size_bytes / size_per_ms)
        logging.info(f"Maximum chunk length: {max_chunk_length_ms / 60000:.2f} minutes")

        base_name = os.path.splitext(os.path.basename(file_path))[0]
        chunks = []
        for i in range(0, total_length_ms, max_chunk_length_ms):
            chunk = audio[i:i+max_chunk_length_ms]
            chunk_filename = f"{base_name}_part{i//max_chunk_length_ms + 1}.wav"
            chunk_path = os.path.join(tmp_dir, chunk_filename)
            chunk.export(chunk_path, format='wav')
            logging.info(f"Exported {chunk_filename}")
            chunks.append(chunk_path)
        return chunks

    except Exception as e:
        logging.exception("An error occurred while splitting the audio file.")
        raise