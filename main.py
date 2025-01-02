# main.py

import uuid
import logging

from logging_config import setup_logging
from audio_text_processor import AudioTextProcessor
from config import (
    DEFAULT_API_URL,
    DEFAULT_AUTHORIZATION,
    DEFAULT_LANGUAGE,
    DEFAULT_TTS_VOICE,
    DEFAULT_USE_VOICE,
    DEFAULT_OUTPUT_DIR
)

def main():
    """
    Main function to execute the AudioTextProcessor.
    """
    # Setup logging
    setup_logging()

    # Define your messages and parameters here
    user_message = "What was the last question I asked you? Also tell me what is your knowledge cut off."
    assistant_message = "Hello! I'm here with you."
    tts_voice = "nova"  
    language = "en"       
    use_voice = True
    play_audio_flag = True 

    # Initialize the processor with appropriate configurations
    processor = AudioTextProcessor(
        app_id=f'anonymous_{uuid.uuid4().hex}',
        language=language,
        tts_voice=tts_voice,
        use_voice=use_voice,
        api_url=DEFAULT_API_URL,
        authorization=DEFAULT_AUTHORIZATION,
        output_dir=DEFAULT_OUTPUT_DIR
    )

    # Generate audio and text based on the messages
    response = processor.generate(
        user_message=user_message,
        assistant_message=assistant_message,
        play_audio=play_audio_flag
    )

    if response:
        logging.info("Processing completed successfully.")
    else:
        logging.error("Processing failed.")

if __name__ == "__main__":
    main()
