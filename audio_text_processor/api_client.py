# audio_text_processor/api_client.py

import json
import logging
from typing import Any, Dict, List, Optional

import requests
from requests_toolbelt import MultipartEncoder

from config.settings import DEFAULT_HEADERS

class APIClient:
    """
    Handles interactions with the Earkick API.
    """

    def __init__(self, api_url: str, authorization: str) -> None:
        """
        Initializes the APIClient with the API URL and authorization.

        Args:
            api_url (str): The API endpoint URL.
            authorization (str): The authorization header value.
        """
        self.api_url = api_url
        self.headers = DEFAULT_HEADERS.copy()
        self.headers['Authorization'] = authorization

    def send_post_request(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Sends a POST request to the API with the given payload.

        Args:
            payload (dict): The payload to send as multipart/form-data.

        Returns:
            dict or None: Parsed JSON response if successful, else None.
        """
        form_data = MultipartEncoder(fields=payload)
        headers = self.headers.copy()
        headers['Content-Type'] = form_data.content_type

        try:
            logging.info("Sending POST request to the API.")
            response = requests.post(self.api_url, headers=headers, data=form_data)
            response.raise_for_status()
            response_data = response.json()
            logging.info("Request successful. Received response.")
            return response_data
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Response Status Code: {e.response.status_code}")
                logging.error(f"Response Body: {e.response.text}")
            return None
        except json.JSONDecodeError:
            logging.error("Failed to parse JSON response.")
            return None
