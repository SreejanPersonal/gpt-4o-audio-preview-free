# GPT-4O Audio Preview Free

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![GitHub Issues](https://img.shields.io/github/issues/SreejanPersonal/gpt-4o-audio-preview-free.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

## Table of Contents

- [GPT-4O Audio Preview Free](#gpt-4o-audio-preview-free)
  - [Table of Contents](#table-of-contents)
  - [File Structure and Logic](#file-structure-and-logic)
    - [Detailed File Overview](#detailed-file-overview)
    - [File Structure Diagram](#file-structure-diagram)
  - [Setup and Installation Guide](#setup-and-installation-guide)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
    - [Configuration](#configuration)
  - [Usage Instructions](#usage-instructions)
    - [Running the Project](#running-the-project)
    - [Features and Functionality](#features-and-functionality)
  - [Contributing Guidelines](#contributing-guidelines)
    - [Contribution Process](#contribution-process)
    - [Code Standards](#code-standards)
  - [Licensing Information](#licensing-information)
  - [Additional Information](#additional-information)
    - [Author Information](#author-information)
    - [Acknowledgments](#acknowledgments)
  
---

## File Structure and Logic

### Detailed File Overview

- **`audio_text_processor/`**
  - **`__init__.py`**
    - Initializes the `audio_text_processor` package and exposes the `AudioTextProcessor` class.
    
    ```python
    from .processor import AudioTextProcessor

    __all__ = ['AudioTextProcessor']
    ```
  
  - **`api_client.py`**
    - Manages interactions with the Earkick API, handling POST requests and response parsing.
    
    ```python
    # Contains the APIClient class for API interactions
    ```
  
  - **`audio_handler.py`**
    - Handles audio decoding, format detection, saving, and playback using the `pydub` library.
    
    ```python
    # Contains the AudioHandler class for audio processing
    ```
  
  - **`processor.py`**
    - Core processor that orchestrates communication with the API and manages audio/text responses.
    
    ```python
    # Contains the AudioTextProcessor class for processing
    ```
  
  - **`utils.py`**
    - Utility functions for decoding Base64 strings and generating unique filenames.
    
    ```python
    # Contains utility functions for decoding and filename generation
    ```

- **`config/`**
  - **`__init__.py`**
    - Initializes the `config` package and exposes configuration settings.
    
    ```python
    from .settings import (
        SUPPORTED_AUDIO_FORMATS,
        DEFAULT_API_URL,
        DEFAULT_AUTHORIZATION,
        DEFAULT_LANGUAGE,
        DEFAULT_TTS_VOICE,
        DEFAULT_USE_VOICE,
        DEFAULT_OUTPUT_DIR,
        DEFAULT_HEADERS
    )

    __all__ = [
        'SUPPORTED_AUDIO_FORMATS',
        'DEFAULT_API_URL',
        'DEFAULT_AUTHORIZATION',
        'DEFAULT_LANGUAGE',
        'DEFAULT_TTS_VOICE',
        'DEFAULT_USE_VOICE',
        'DEFAULT_OUTPUT_DIR',
        'DEFAULT_HEADERS'
    ]
    ```
  
  - **`settings.py`**
    - Defines default settings and supported audio formats for the application.
    
    ```python
    # Contains configuration settings for the application
    ```

- **`logging_config.py`**
  - Configures the logging mechanism for the application, directing logs to both the console and a log file.
  
  ```python
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
  ```

- **`main.py`**
  - Entry point of the application. Initializes the `AudioTextProcessor` and executes the processing workflow based on predefined messages.
  
  ```python
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
  ```

- **`output/`**
  - **`response_audio_converted_79b8a3379944494d8d6e2f601884442c.mp3`**
    - Generated audio file from the processing workflow.
  
    > ⚠️ Unable To Read File Contents : 'utf-8' codec can't decode byte 0xff in position 44: invalid start byte

- **`requirements.txt`**
  - Lists all Python dependencies required to run the project.
  
  ```text
  pydub==0.25.1
  Requests==2.32.3
  requests_toolbelt==1.0.0
  ```

- **`audio_text_processor.log`**
  - Log file capturing the application's runtime events and errors.
  
  ```
  2025-01-02 17:52:11,563 - INFO - Output directory set to: output
  2025-01-02 17:52:11,563 - INFO - AudioTextProcessor initialized successfully.
  2025-01-02 17:52:11,565 - INFO - Sending POST request to the API.
  2025-01-02 17:52:18,674 - INFO - Request successful. Received response.
  2025-01-02 17:52:18,676 - INFO - Extracted Messages:
  2025-01-02 17:52:18,679 - INFO - Audio data successfully decoded from Base64.
  2025-01-02 17:52:18,679 - WARNING - Unknown audio format based on magic numbers.
  2025-01-02 17:52:18,679 - WARNING - Unknown audio format. Attempting to convert to MP3.
  2025-01-02 17:52:19,857 - INFO - Audio converted and saved as output\response_audio_converted_79b8a3379944494d8d6e2f601884442c.mp3
  2025-01-02 17:52:19,858 - INFO - Playing audio file: output\response_audio_converted_79b8a3379944494d8d6e2f601884442c.mp3
  2025-01-02 17:52:35,934 - INFO - Audio playback completed.
  2025-01-02 17:52:35,936 - INFO - Audio processing completed. File saved at: output\response_audio_converted_79b8a3379944494d8d6e2f601884442c.mp3
  2025-01-02 17:52:35,936 - INFO - Processing completed successfully.
  ```

---

## File Structure Diagram

```
gpt-4o-audio-preview-free/
├── audio_text_processor/
│   ├── __init__.py
│   ├── api_client.py
│   ├── audio_handler.py
│   ├── processor.py
│   └── utils.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── logging_config.py
├── main.py
├── output/
│   └── response_audio_converted_79b8a3379944494d8d6e2f601884442c.mp3
├── requirements.txt
└── audio_text_processor.log
```

---

## Setup and Installation Guide

### Prerequisites

Ensure the following software and tools are installed on your local machine:

- **Python**: Version 3.9 or higher. [Download Python](https://www.python.org/downloads/)
- **pip**: Python package installer. Comes bundled with Python.
- **Git**: Version control system. [Download Git](https://git-scm.com/)
- **FFmpeg**: Required by `pydub` for audio processing. [Download FFmpeg](https://ffmpeg.org/download.html)

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/SreejanPersonal/gpt-4o-audio-preview-free.git
   cd gpt-4o-audio-preview-free
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Install FFmpeg**

   Ensure FFmpeg is installed and added to your system's PATH. You can verify the installation by running:

   ```bash
   ffmpeg -version
   ```

### Configuration

1. **Environment Variables**

   Create a `.env` file in the root directory (if applicable) and add the necessary environment variables. Alternatively, modify the `config/settings.py` file directly.

   ```env
   # Example .env file
   API_URL=https://ml-demo.earkick.com/web-chat/audio/audio_generate
   AUTHORIZATION=Basic d2ViY2hhdDphd0NpcG1pa0lidXBoQXJuRWtCYWJNeXNVZHNvZHV0amFodXJFZWM6
   LANGUAGE=en
   TTS_VOICE=nova
   USE_VOICE=True
   OUTPUT_DIR=output
   ```

2. **Adjust Configuration Settings**

   Modify the `config/settings.py` file to adjust settings as needed:

   ```python
   SUPPORTED_AUDIO_FORMATS = {
       'mp3': 'mp3',
       'wav': 'wav',
       'ogg': 'ogg',
       'flac': 'flac',
       'm4a': 'm4a'
   }

   DEFAULT_API_URL = 'https://ml-demo.earkick.com/web-chat/audio/audio_generate'
   DEFAULT_AUTHORIZATION = 'Your_Authorization_Key'
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
   ```

---

## Usage Instructions

### Running the Project

To start the application, ensure your virtual environment is activated and run:

```bash
python main.py
```

This will execute the `main.py` script, which initializes the `AudioTextProcessor`, sends a request to the Earkick API, processes the response, and handles audio playback.

### Features and Functionality

- **User Interaction**
  - Sends user messages to the Earkick API and receives assistant responses.
  
- **Audio Processing**
  - Decodes Base64-encoded audio responses.
  - Detects audio formats and converts them to MP3 if necessary.
  - Saves audio files to the specified output directory.
  - Plays audio responses automatically based on configuration.
  
- **Logging**
  - Logs detailed information and errors to both the console and a log file (`audio_text_processor.log`).
  
- **Configuration**
  - Easily configurable settings for API endpoints, authorization, language, TTS voice, and more.

---

## Contributing Guidelines

### Contribution Process

We welcome contributions from the community! To contribute:

1. **Fork the Repository**

   Click the "Fork" button at the top-right corner of the repository page.

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add your detailed description here"
   ```

4. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Open a Pull Request**

   Navigate to the original repository and click "New Pull Request". Provide a clear description of your changes.

### Code Standards

Please adhere to the following coding standards:

- **Language**: Python 3.9+
- **Style Guide**: [PEP 8](https://pep8.org/)
- **Linting**: Ensure code passes all linting checks by running:

  ```bash
  pip install flake8
  flake8 .
  ```

- **Testing**: Include relevant unit tests for new features and ensure all existing tests pass.

  ```bash
  # Example: If using unittest
  python -m unittest discover tests
  ```

- **Documentation**: Update documentation and comments to reflect code changes.

---

## Licensing Information

This project is licensed under the [MIT License](LICENSE).

---

## Additional Information

### Author Information

- **GitHub**: [SreejanPersonal](https://github.com/SreejanPersonal)
- **YouTube**: [DevsDoCode](https://www.youtube.com/channel/DevsDoCode)

### Acknowledgments

- **Libraries & Frameworks**
  - [pydub](https://github.com/jiaaro/pydub) for audio processing.
  - [Requests](https://requests.readthedocs.io/) for handling HTTP requests.
  - [Requests-Toolbelt](https://toolbelt.readthedocs.io/) for advanced HTTP utilities.
  
- **Resources**
  - [MDN Web Docs](https://developer.mozilla.org/) for comprehensive web development documentation.
  - [Stack Overflow](https://stackoverflow.com/) for community-driven programming help.
  
- **Contributors**
  - Thanks to all the contributors who have helped improve this project!

---

*This README was crafted with precision and care by [SreejanPersonal](https://github.com/SreejanPersonal).*