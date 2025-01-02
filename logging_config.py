import logging
import os

def setup_logging(log_file: str = 'audio_text_processor.log') -> None:
    """
    Configures the logging for the application.

    Args:
        log_file (str): The filename for the log file.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding='utf-8')
        ]
    )
