# audio_text_processor/audio_handler.py

import io
import logging
import os
from typing import Optional

from pydub import AudioSegment
from pydub.playback import play

from audio_text_processor.utils import decode_base64, generate_unique_filename
from config.settings import SUPPORTED_AUDIO_FORMATS

class AudioHandler:
    """
    Handles audio decoding, format detection, saving, and playback.
    """

    def __init__(self, output_dir: str) -> None:
        """
        Initializes the AudioHandler with the output directory.

        Args:
            output_dir (str): Directory to save audio files.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logging.info(f"Output directory set to: {self.output_dir}")

    def process_audio(self, audio_base64: str, play_audio: bool = False) -> Optional[str]:
        """
        Processes the audio data from Base64 string.

        Args:
            audio_base64 (str): Base64-encoded audio string.
            play_audio (bool): Flag to play audio after saving.

        Returns:
            str or None: Path to the saved audio file if successful, else None.
        """
        audio_bytes = decode_base64(audio_base64)
        if not audio_bytes:
            logging.error("Decoded audio bytes are empty.")
            return None
        logging.info("Audio data successfully decoded from Base64.")

        audio_format = self.detect_audio_format(audio_bytes)
        if audio_format:
            filename = generate_unique_filename(extension=audio_format)
            audio_file_path = os.path.join(self.output_dir, filename)
            try:
                with open(audio_file_path, 'wb') as audio_file:
                    audio_file.write(audio_bytes)
                logging.info(f"Audio saved as {audio_file_path}")
            except IOError as e:
                logging.error(f"Failed to write audio file: {e}")
                return None
        else:
            logging.warning("Unknown audio format. Attempting to convert to MP3.")
            try:
                audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
                filename = generate_unique_filename(prefix='response_audio_converted', extension='mp3')
                audio_file_path = os.path.join(self.output_dir, filename)
                audio.export(audio_file_path, format='mp3')
                logging.info(f"Audio converted and saved as {audio_file_path}")
            except Exception as e:
                logging.error(f"Failed to convert audio: {e}")
                return None

        if play_audio:
            self.play_audio(audio_file_path)
        else:
            logging.info("Audio playback skipped.")

        return audio_file_path

    def detect_audio_format(self, audio_bytes: bytes) -> Optional[str]:
        """
        Detects the audio format based on magic numbers.

        Args:
            audio_bytes (bytes): The decoded audio data.

        Returns:
            str or None: The detected audio format extension, or None if unknown.
        """
        if audio_bytes.startswith(b'ID3') or audio_bytes.startswith(b'\xFF\xFB'):
            logging.info("Detected audio format: MP3")
            return SUPPORTED_AUDIO_FORMATS['mp3']
        elif audio_bytes.startswith(b'RIFF') and b'WAVE' in audio_bytes[8:12]:
            logging.info("Detected audio format: WAV")
            return SUPPORTED_AUDIO_FORMATS['wav']
        elif audio_bytes.startswith(b'OggS'):
            logging.info("Detected audio format: OGG")
            return SUPPORTED_AUDIO_FORMATS['ogg']
        elif audio_bytes.startswith(b'fLaC'):
            logging.info("Detected audio format: FLAC")
            return SUPPORTED_AUDIO_FORMATS['flac']
        elif audio_bytes.startswith(b'ftyp'):
            logging.info("Detected audio format: MP4/M4A")
            return SUPPORTED_AUDIO_FORMATS['m4a']
        else:
            logging.warning("Unknown audio format based on magic numbers.")
            return None

    def play_audio(self, file_path: str) -> None:
        """
        Plays the audio file using pydub's playback module.

        Args:
            file_path (str): Path to the audio file.
        """
        try:
            logging.info(f"Playing audio file: {file_path}")
            audio = AudioSegment.from_file(file_path)
            play(audio)
            logging.info("Audio playback completed.")
        except Exception as e:
            logging.error(f"Failed to play audio file: {e}")
