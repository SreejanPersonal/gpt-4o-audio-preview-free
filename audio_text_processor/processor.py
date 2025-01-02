# audio_text_processor/processor.py

import json
import logging
import os
import uuid
from typing import Any, Dict, List, Optional

from audio_text_processor.api_client import APIClient
from audio_text_processor.audio_handler import AudioHandler
from config.settings import (
    DEFAULT_LANGUAGE,
    DEFAULT_TTS_VOICE,
    DEFAULT_USE_VOICE
)

class AudioTextProcessor:
    """
    A professional handler for interacting with the Earkick API to process textual and audio responses.
    """

    def __init__(
        self,
        app_id: str,
        language: str = DEFAULT_LANGUAGE,
        tts_voice: str = DEFAULT_TTS_VOICE,
        use_voice: bool = DEFAULT_USE_VOICE,
        api_url: str = '',
        authorization: str = '',
        output_dir: str = 'output'
    ) -> None:
        """
        Initializes the AudioTextProcessor with necessary configurations.

        Args:
            app_id (str): The application ID for authentication.
            language (str, optional): The language code (default is 'en').
            tts_voice (str, optional): The text-to-speech voice identifier (default is 'nova').
            use_voice (bool, optional): Flag to use voice synthesis (default is True).
            api_url (str, optional): The API endpoint URL.
            authorization (str, optional): The authorization header value.
            output_dir (str, optional): Directory to save outputs.
        """
        self.api_url = api_url
        self.app_id = app_id
        self.language = language
        self.tts_voice = tts_voice
        self.use_voice = use_voice
        self.authorization = authorization
        self.output_dir = output_dir

        # Initialize API client and Audio handler
        self.api_client = APIClient(api_url=self.api_url, authorization=self.authorization)
        self.audio_handler = AudioHandler(output_dir=self.output_dir)

        logging.info("AudioTextProcessor initialized successfully.")

    def generate(
        self,
        user_message: str,
        assistant_message: Optional[str] = None,
        tts_voice: Optional[str] = None,
        language: Optional[str] = None,
        use_voice: Optional[bool] = None,
        play_audio: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Generates textual and audio responses from the Earkick API.

        Args:
            user_message (str): The user's message to send.
            assistant_message (str, optional): Previous assistant message for context.
            tts_voice (str, optional): Override the default TTS voice.
            language (str, optional): Override the default language.
            use_voice (bool, optional): Override the default voice usage flag.
            play_audio (bool, optional): Whether to play the audio automatically (default is False).

        Returns:
            dict or None: Parsed JSON response from the API if successful, else None.
        """
        user_messages = [{"role": "user", "content": user_message}]
        assistant_messages_list = [{"role": "assistant", "content": assistant_message}] if assistant_message else []

        payload = self._prepare_payload(user_messages, assistant_messages_list, tts_voice, language, use_voice)
        response_data = self.api_client.send_post_request(payload)

        if response_data:
            self._process_response(response_data, play_audio)
            return response_data
        else:
            logging.error("No response data to process.")
            return None

    def _prepare_payload(
        self, 
        user_messages: List[Dict[str, str]], 
        assistant_messages: List[Dict[str, str]],
        tts_voice: Optional[str],
        language: Optional[str],
        use_voice: Optional[bool]
    ) -> Dict[str, Any]:
        """
        Prepares the multipart form data payload.

        Args:
            user_messages (list): List of user messages.
            assistant_messages (list): List of assistant messages.
            tts_voice (str, optional): Override TTS voice.
            language (str, optional): Override language.
            use_voice (bool, optional): Override voice usage flag.

        Returns:
            dict: Dictionary containing form fields.
        """
        messages = assistant_messages + user_messages

        payload = {
            'app_id': self.app_id,
            'language': language if language is not None else self.language,
            'tts_voice': tts_voice if tts_voice is not None else self.tts_voice,
            'voice': str(use_voice).lower() if use_voice is not None else str(self.use_voice).lower(),
            'messages': json.dumps(messages)
        }
        logging.debug(f"Prepared payload: {payload}")
        return payload

    def _process_response(self, data: Dict[str, Any], play_audio_flag: bool) -> None:
        """
        Processes the API response by extracting messages and audio.

        Args:
            data (dict): Parsed JSON response from the API.
            play_audio_flag (bool): Whether to play the audio automatically.
        """
        self._extract_and_display_messages(data)
        self._extract_and_save_audio(data, play_audio_flag)

    def _extract_and_display_messages(self, data: Dict[str, Any]) -> None:
        """
        Extracts and displays the messages from the response.

        Args:
            data (dict): Parsed JSON response from the API.
        """
        messages = data.get('messages', [])
        if not messages:
            logging.warning("No messages found in the response.")
            return

        logging.info("Extracted Messages:")
        for message in messages:
            role = message.get('role', 'Unknown').capitalize()
            content = message.get('content', '')
            print(f"{role}: {content}")

    def _extract_and_save_audio(self, data: Dict[str, Any], play_audio_flag: bool) -> None:
        """
        Extracts the audio data, decodes it, detects its format, and saves it appropriately.

        Args:
            data (dict): Parsed JSON response from the API.
            play_audio_flag (bool): Whether to play the audio automatically.
        """
        audio_base64 = data.get('audio')
        if not audio_base64:
            logging.warning("No audio data found in the response.")
            return

        audio_file_path = self.audio_handler.process_audio(audio_base64, play_audio=play_audio_flag)
        if audio_file_path:
            logging.info(f"Audio processing completed. File saved at: {audio_file_path}")
        else:
            logging.error("Audio processing failed.")
