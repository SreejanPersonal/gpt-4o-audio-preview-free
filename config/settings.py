from dotenv import load_dotenv; load_dotenv()
import os

SUPPORTED_AUDIO_FORMATS = {
    'mp3': 'mp3',
    'wav': 'wav',
    'ogg': 'ogg',
    'flac': 'flac',
    'm4a': 'm4a'
}

DEFAULT_API_URL = 'https://ml-demo.earkick.com/web-chat/audio/audio_generate'
DEFAULT_AUTHORIZATION = f'Basic {os.getenv("EARKICK_API_KEY")}'
DEFAULT_LANGUAGE = 'en'
DEFAULT_TTS_VOICE = 'nova'
DEFAULT_USE_VOICE = True
DEFAULT_OUTPUT_DIR = 'output'

DEFAULT_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    'DNT': '1',
    'Origin': 'https://earkick.com',
    'Referer': 'https://earkick.com/',
    'Sec-CH-UA': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'Sec-CH-UA-Mobile': '?0',
    'Sec-CH-UA-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/131.0.0.0 Safari/537.36'
}
