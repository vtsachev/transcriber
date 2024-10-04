# transcript_processor.py

import logging
import tiktoken

def process_transcript(client, transcript_text, output_file_name):
    """
    Processes the combined transcript with GPT-4o-mini in manageable chunks and saves the final transcript.

    Parameters:
    - client: OpenAI client object
    - transcript_text: The combined transcript text.
    - output_file_name: The filename to save the final transcript.
    """
    try:
        # Your specified prompt
        prompt = """
Your task is to improve the readability of a raw transcript while preserving as much of the original wording as possible. Follow these guidelines:

1. Read the transcript carefully, sentence by sentence.
2. Identify speakers:
   - There are multiple potential speakers in this transcript.
   - Identify transitions between speakers based on:
     a) Clear changes in the topic or subject matter
     b) Shifts in speaking style, vocabulary, or tone
     c) Contextual clues indicating a new person is speaking (e.g., "Thank you for that presentation, now I have a question...")
   - Assign content to speakers as follows:
     a) For consecutive content from the same speaker, group it together.
     b) When you detect a likely speaker change, start a new paragraph and label it with a new speaker designation.
   - Label speakers sequentially as "Speaker 1", "Speaker 2", "Speaker 3", etc., in the order they appear in the transcript.
   - If a speaker returns later in the transcript, reuse their original label.
   - If you're unsure about a speaker change, err on the side of keeping the current speaker label.

3. Improve readability with minimal changes:
   - Correct only obvious grammatical errors and typos.
   - Retain original wording unless it significantly impairs understanding.
   - Keep filler words and false starts unless they severely disrupt readability.
   - Only break up extremely long, confusing sentences if necessary for comprehension.
   - Maintain the original tone, style, and vocabulary of each speaker.

4. Handle unclear or nonsensical parts:
   - If a part is completely incomprehensible, replace it with [best guess].
   - Inside the brackets, provide your best interpretation of the intended meaning.
   - Use a similar number of words and try to incorporate any recognizable parts of the original text.

5. Formatting:
   - Present the transcript in a clear, easy-to-read format.
   - Start a new paragraph for each change of speaker.

6. Prioritize authenticity:
   - Your primary goal is to preserve the original content as much as possible.
   - Make only the minimum changes necessary for basic comprehension.
   - Do not add new information, elaborate, or change the context of the conversation.
   - If in doubt, keep the original wording.

Provide the minimally-edited, more readable version of the transcript while strictly adhering to these guidelines. The output should be nearly identical to the input, with changes only where absolutely necessary for basic understanding.
"""

        # Maximum tokens for GPT-4o-mini
        MAX_CONTEXT_LENGTH = 128000
        MAX_COMPLETION_TOKENS = 16384  # Model's maximum output tokens
        MAX_INPUT_TOKENS = MAX_CONTEXT_LENGTH - MAX_COMPLETION_TOKENS

        # Initialize the tiktoken encoder
        encoding = tiktoken.encoding_for_model("gpt-4o-mini")

        # Tokenize the prompt and system message
        prompt_tokens = len(encoding.encode(prompt))
        system_message_tokens = len(encoding.encode("You are a helpful assistant."))

        # Calculate available tokens for the transcript
        available_tokens = MAX_INPUT_TOKENS - prompt_tokens - system_message_tokens - 100  # Reserve some buffer

        # Split the transcript into chunks that fit within the available tokens
        transcript_chunks = split_transcript_into_chunks(transcript_text, available_tokens, encoding)

        # Process each chunk
        final_transcript = ""
        chunk_number = 1

        for chunk in transcript_chunks:
            logging.info(f"Processing chunk {chunk_number}/{len(transcript_chunks)}")

            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt + "\n\n" + chunk}
            ]

            # Estimate the total tokens for this request
            total_request_tokens = prompt_tokens + system_message_tokens + len(encoding.encode(chunk))

            # Adjust max_tokens to prevent exceeding the context window
            max_tokens_for_completion = min(MAX_COMPLETION_TOKENS, MAX_CONTEXT_LENGTH - total_request_tokens - 100)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=max_tokens_for_completion,
                temperature=0.5
            )

            # Extract the assistant's reply
            assistant_reply = response.choices[0].message.content

            final_transcript += assistant_reply + "\n"

            chunk_number += 1

        # Save the final transcript
        with open(output_file_name, "w", encoding="utf-8") as f:
            f.write(final_transcript)
        logging.info(f"Final transcript saved to '{output_file_name}'")

    except Exception as e:
        logging.exception("An unexpected error occurred during processing with GPT-4o-mini.")
        raise

def split_transcript_into_chunks(transcript_text, max_tokens_per_chunk, encoding):
    """
    Splits the transcript text into chunks that do not exceed the max tokens per chunk.

    Parameters:
    - transcript_text: The combined transcript text.
    - max_tokens_per_chunk: Maximum number of tokens allowed per chunk.
    - encoding: The tiktoken encoding object.

    Returns:
    - List of transcript text chunks.
    """
    # Split the transcript into sentences or paragraphs
    import re
    sentences = re.split(r'(?<=[.!?])\s+', transcript_text)

    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(encoding.encode(sentence))

        if current_tokens + sentence_tokens <= max_tokens_per_chunk:
            current_chunk += sentence + " "
            current_tokens += sentence_tokens
        else:
            # Start a new chunk
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
            current_tokens = sentence_tokens

            # Handle sentences longer than max_tokens_per_chunk
            if sentence_tokens > max_tokens_per_chunk:
                logging.warning(f"A single sentence exceeds the maximum tokens per chunk: '{sentence[:50]}...'")
                # You may choose to split the sentence further or handle it accordingly

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks