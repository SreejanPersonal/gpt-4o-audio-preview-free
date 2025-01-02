# audio_text_processor/utils.py

import base64
import logging
import uuid
from typing import Optional

def decode_base64(data: str) -> Optional[bytes]:
    """
    Decodes a Base64-encoded string, handling padding if necessary.

    Args:
        data (str): Base64-encoded string.

    Returns:
        bytes or None: Decoded bytes if successful, else None.
    """
    try:
        padding_needed = 4 - (len(data) % 4)
        if padding_needed and padding_needed != 4:
            data += '=' * padding_needed
        return base64.b64decode(data, validate=True)
    except (base64.binascii.Error, ValueError) as e:
        logging.error(f"Base64 decoding failed: {e}")
        return None

def generate_unique_filename(prefix: str = 'response_audio', extension: str = 'mp3') -> str:
    """
    Generates a unique filename using UUID.

    Args:
        prefix (str): Prefix for the filename.
        extension (str): File extension.

    Returns:
        str: Unique filename.
    """
    return f"{prefix}_{uuid.uuid4().hex}.{extension}"
