import os
import asyncio
from googletrans import Translator
from gtts import gTTS
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize translator
translator = Translator()

async def translate_to_hindi(text: str) -> str:
    """
    Translate the given text to Hindi asynchronously using googletrans.
    
    Args:
        text (str): The text to translate.
        
    Returns:
        str: Translated text in Hindi.
    """
    try:
        # Translate the text to Hindi
        translated = await translator.translate(text, src='en', dest='hi')
        return translated.text
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        return None

async def generate_hindi_audio(text: str, output_file: str = "hindi_audio.mp3") -> Optional[str]:
    """
    Generate a Hindi audio file from the given text using gTTS.
    
    Args:
        text (str): The text to convert to speech.
        output_file (str): The name of the output audio file.
        
    Returns:
        str: Path to the generated audio file.
        None: If TTS generation fails.
    """
    try:
        # Generate Hindi audio using gTTS
        tts = gTTS(text, lang='hi')
        tts.save(output_file)
        return output_file
    except Exception as e:
        logger.error(f"TTS generation failed: {str(e)}")
        return None

async def translate_and_generate_audio(text: str, output_file: str = "hindi_audio.mp3") -> Optional[str]:
    """
    Translate the text to Hindi and generate an audio file asynchronously.
    
    Args:
        text (str): The text to translate and convert to speech.
        output_file (str): The name of the output audio file.
        
    Returns:
        str: Path to the generated audio file.
        None: If translation or TTS generation fails.
    """
    try:
        # Translate the text to Hindi
        hindi_text = await translate_to_hindi(text)
        if not hindi_text:
            logger.error("Translation failed.")
            return None
        
        # Generate Hindi audio
        audio_file = await generate_hindi_audio(hindi_text, output_file)
        if not audio_file:
            logger.error("TTS generation failed.")
            return None
        
        return audio_file
    except Exception as e:
        logger.error(f"Failed to translate and generate audio: {str(e)}")
        return None

# Example usage
async def main():
    # Test with sample data
    overall_summary = "Reliance Industries has shown strong financial performance this quarter, with a 20% increase in profits. The company's announcement to expand into European markets further underscores its growth trajectory. However, it faces criticism from environmental groups regarding its carbon emissions. The overall sentiment score is 0.3"
    
    # Translate and generate audio
    audio_file = await translate_and_generate_audio(overall_summary)
    if audio_file:
        print(f"Audio file generated: {audio_file}")
    else:
        print("Failed to generate audio file.")

if __name__ == "__main__":
    asyncio.run(main())