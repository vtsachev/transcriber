# Audio Transcription and Processing Tool

A Python application that transcribes audio files into text using OpenAI's Whisper model and processes transcripts using GPT-4o-mini. This tool supports various audio formats and allows for both audio transcription and transcript formatting.

## Features

- **Audio Transcription**: Convert audio files into text using OpenAI's Whisper API.
- **Transcript Processing**: Enhance readability and structure of transcripts using GPT-4o-mini.
- **Supports Multiple Audio Formats**: Works with common audio file types.
- **Modular Design**: Clean and maintainable codebase with separated concerns.
- **Output Management**: Prevents overwriting by generating unique filenames and organizes outputs into dedicated directories.

## Requirements

- Python 3.7 or higher
- An OpenAI API key with access to the Whisper and GPT-4o-mini models

### Python Packages

Listed in `requirements.txt`:

- pydub
- openai
- tiktoken

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. Create a virtual environment (optional but recommended):

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

## Setup

### OpenAI API Key

The application requires an OpenAI API key to access the transcription and language models.

1. Obtain an API Key:
   - Sign up for an account at OpenAI.
   - Navigate to the API Keys section.
   - Create a new secret key.

2. Set the API Key as an Environment Variable:
   - On macOS/Linux:
     ```
     export OPENAI_API_KEY='your-api-key-here'
     ```
   - On Windows (Command Prompt):
     ```
     set OPENAI_API_KEY='your-api-key-here'
     ```
   - On Windows (PowerShell):
     ```
     $env:OPENAI_API_KEY='your-api-key-here'
     ```

   Replace 'your-api-key-here' with your actual API key.

## Usage

The application can process both audio files and existing transcripts.

### Processing an Audio File

Transcribe an audio file and process the transcript.

```
python main.py path_to_audio_file
```

Example:

```
python main.py audio_files/meeting_recording.mp3
```

### Processing a Transcript File

Process an existing transcript to enhance readability and structure.

```
python main.py path_to_transcript_file --transcript
```

Example:

```
python main.py transcripts/raw_transcript.txt --transcript
```

### Supported Audio Formats

The application supports the following audio file formats:

- mp3
- mp4
- mpeg
- mpga
- m4a
- wav
- webm

## Output

- **Raw Transcripts**:
  - Saved in the `raw_transcripts/` directory.
  - Filenames include the audio file's name.
  - If a file with the same name exists, a numbered suffix is added (e.g., `meeting_recording.txt`, `meeting_recording_1.txt`).
- **Processed Transcripts**:
  - Saved in the `transcripts/` directory.
  - Filenames include the base name of the input file.
  - Numbered suffixes are added to prevent overwriting existing files.

## OpenAI Models Used

- **Transcription**: `whisper-1`
  - Used to transcribe audio files into text.
- **Transcript Processing**: `gpt-4o-mini`
  - Enhances the readability and structure of transcripts.

## Application Structure

The application is designed with modularity in mind, separating concerns across different modules.

### Modules

- `main.py`:
  - Entry point of the application.
  - Handles argument parsing and initializes the application.
- `app.py`:
  - Contains the `TranscriberApp` class.
  - Manages the core workflow for processing audio and transcript files.
- `file_manager.py`:
  - Handles file and directory operations.
  - Creates necessary directories and manages unique filenames.
- `logger_config.py`:
  - Configures logging for the application.
  - Ensures logs are output to the console.
- `api_validator.py`:
  - Validates the OpenAI API key by making a test API call.
- `audio_splitter.py`:
  - Splits large audio files into smaller chunks if necessary.
- `audio_transcriber.py`:
  - Transcribes audio files using the OpenAI Whisper API.
- `transcript_processor.py`:
  - Processes transcripts with GPT-4o-mini to enhance readability and structure.

### Directory Structure

```
├── audio_files/           # Place your audio files here
├── raw_transcripts/       # Stores raw transcripts generated from audio files
├── transcripts/           # Stores processed transcripts
├── tmp/                   # Temporary files
├── main.py                # Entry point of the application
├── app.py                 # Core application logic
├── file_manager.py        # File and directory management
├── logger_config.py       # Logging configuration
├── api_validator.py       # API key validation
├── audio_splitter.py      # Audio splitting logic
├── audio_transcriber.py   # Audio transcription logic
├── transcript_processor.py# Transcript processing logic
├── requirements.txt       # Python package requirements
```
