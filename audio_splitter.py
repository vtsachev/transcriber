import os
import logging
from pydub import AudioSegment

def split_audio(file_path, tmp_dir):
    """
    Splits the audio file into chunks less than 24 MB and saves them in the tmp directory.

    Parameters:
    - file_path: Path to the audio file.
    - tmp_dir: Directory to save the split audio chunks.

    Returns:
    - chunks: List of paths to the audio files (original file or split chunks).
    """
    try:
        # Define maximum chunk size with a safety margin (24 MB instead of 25 MB)
        max_chunk_size_bytes = 24 * 1024 * 1024  # 24 MB

        # Load the audio file
        audio = AudioSegment.from_file(file_path)
        total_length_ms = len(audio)
        logging.info(f"Total audio length: {total_length_ms / 60000:.2f} minutes")

        # Get audio properties
        frame_rate = audio.frame_rate
        sample_width = audio.sample_width  # in bytes
        channels = audio.channels
        frame_width = audio.frame_width  # sample_width * channels
        bytes_per_second = frame_rate * frame_width
        logging.info(f"Audio properties - Frame rate: {frame_rate}, Sample width: {sample_width}, Channels: {channels}")

        # Calculate maximum chunk length to be under 24 MB
        max_chunk_length_sec = max_chunk_size_bytes / bytes_per_second
        max_chunk_length_ms = int(max_chunk_length_sec * 1000)
        logging.info(f"Maximum chunk length: {max_chunk_length_ms / 60000:.2f} minutes")

        base_name = os.path.splitext(os.path.basename(file_path))[0]
        chunks = []
        i = 0
        part_num = 1
        while i < total_length_ms:
            chunk_length_ms = max_chunk_length_ms
            while True:
                chunk = audio[i:i+chunk_length_ms]
                # Export the chunk to a temporary file to get its actual size
                chunk_filename = f"{base_name}_part{part_num}.wav"
                chunk_path = os.path.join(tmp_dir, chunk_filename)
                chunk.export(chunk_path, format='wav')

                chunk_size = os.path.getsize(chunk_path)
                if chunk_size > max_chunk_size_bytes:
                    # Reduce the chunk length by 10% and retry
                    logging.warning(f"Chunk '{chunk_filename}' is too large ({chunk_size / (1024 * 1024):.2f} MB). Reducing chunk length.")
                    os.remove(chunk_path)
                    chunk_length_ms = int(chunk_length_ms * 0.9)
                    if chunk_length_ms <= 1000:  # Prevent infinite loop
                        logging.error("Cannot split audio into small enough chunks under the size limit.")
                        raise ValueError("Chunk size exceeds limit even after reduction.")
                else:
                    logging.info(f"Exported '{chunk_filename}' ({chunk_size / (1024 * 1024):.2f} MB)")
                    chunks.append(chunk_path)
                    break
            i += chunk_length_ms
            part_num += 1
        return chunks

    except Exception as e:
        logging.exception("An error occurred while splitting the audio file.")
        raise