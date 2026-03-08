"""
JanSahay AI - Voice Processing Service
ASR (Speech-to-Text) and TTS (Text-to-Speech) with Indian accent optimization.
Supports Google Cloud Speech API with mock fallback for development.
"""

import base64
import io
import json
import logging
from typing import Optional, Tuple
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Language code mapping for Google Cloud Speech
LANGUAGE_CODES = {
    "en": "en-IN",   # English (India)
    "hi": "hi-IN",   # Hindi
    "bn": "bn-IN",   # Bengali
    "ta": "ta-IN",   # Tamil
    "te": "te-IN",   # Telugu
    "mr": "mr-IN",   # Marathi
}

# TTS voice mapping
TTS_VOICES = {
    "en": {"name": "en-IN-Wavenet-A", "gender": "FEMALE"},
    "hi": {"name": "hi-IN-Wavenet-A", "gender": "FEMALE"},
    "bn": {"name": "bn-IN-Wavenet-A", "gender": "FEMALE"},
    "ta": {"name": "ta-IN-Wavenet-A", "gender": "FEMALE"},
    "te": {"name": "te-IN-Wavenet-A", "gender": "FEMALE"},
    "mr": {"name": "mr-IN-Wavenet-A", "gender": "FEMALE"},
}


class VoiceService:
    """
    Voice processing service supporting ASR and TTS.
    Uses Google Cloud Speech APIs with mock fallbacks.
    """

    def __init__(self):
        self._speech_client = None
        self._tts_client = None
        self._use_mock = settings.GOOGLE_CLOUD_PROJECT_ID is None

        if not self._use_mock:
            try:
                from google.cloud import speech_v1 as speech
                from google.cloud import texttospeech_v1 as tts
                self._speech_client = speech.SpeechClient()
                self._tts_client = tts.TextToSpeechClient()
                logger.info("Google Cloud Speech clients initialized")
            except ImportError:
                logger.warning("Google Cloud Speech libraries not installed. Using mock mode.")
                self._use_mock = True
            except Exception as e:
                logger.warning(f"Failed to init Google Cloud Speech: {e}. Using mock mode.")
                self._use_mock = True

    async def speech_to_text(
        self,
        audio_base64: str,
        language: str = "hi",
        audio_format: str = "wav",
    ) -> Tuple[str, str, float]:
        """
        Convert speech audio to text.

        Args:
            audio_base64: Base64-encoded audio data
            language: Language code (en, hi, bn, ta, te, mr)
            audio_format: Audio format (wav, mp3, ogg, webm)

        Returns:
            Tuple of (transcribed_text, detected_language, confidence)
        """
        if self._use_mock:
            return self._mock_speech_to_text(language)

        try:
            from google.cloud import speech_v1 as speech

            audio_bytes = base64.b64decode(audio_base64)
            lang_code = LANGUAGE_CODES.get(language, "hi-IN")

            # Configure recognition
            encoding_map = {
                "wav": speech.RecognitionConfig.AudioEncoding.LINEAR16,
                "mp3": speech.RecognitionConfig.AudioEncoding.MP3,
                "ogg": speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
                "webm": speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            }

            config = speech.RecognitionConfig(
                encoding=encoding_map.get(audio_format, speech.RecognitionConfig.AudioEncoding.LINEAR16),
                sample_rate_hertz=16000,
                language_code=lang_code,
                alternative_language_codes=[
                    code for code in LANGUAGE_CODES.values() if code != lang_code
                ],
                enable_automatic_punctuation=True,
                model="latest_long",
                use_enhanced=True,
                speech_contexts=[
                    speech.SpeechContext(
                        phrases=[
                            "योजना", "पात्रता", "आधार", "राशन कार्ड",
                            "प्रधानमंत्री", "किसान", "आय", "आवेदन",
                            "scheme", "eligible", "document", "apply",
                        ],
                        boost=15.0,
                    )
                ],
            )

            audio = speech.RecognitionAudio(content=audio_bytes)
            response = self._speech_client.recognize(config=config, audio=audio)

            if response.results:
                result = response.results[0]
                transcript = result.alternatives[0].transcript
                confidence = result.alternatives[0].confidence
                detected_lang = result.language_code if hasattr(result, 'language_code') else language
                return transcript, detected_lang, confidence

            return "", language, 0.0

        except Exception as e:
            logger.error(f"ASR error: {e}")
            return self._mock_speech_to_text(language)

    async def text_to_speech(
        self,
        text: str,
        language: str = "hi",
        speed: float = 1.0,
    ) -> Optional[str]:
        """
        Convert text to speech audio.

        Args:
            text: Text to synthesize
            language: Language code
            speed: Speaking rate (0.5 to 2.0)

        Returns:
            Base64-encoded audio data (MP3)
        """
        if self._use_mock:
            return self._mock_text_to_speech(text, language)

        try:
            from google.cloud import texttospeech_v1 as tts

            lang_code = LANGUAGE_CODES.get(language, "hi-IN")
            voice_config = TTS_VOICES.get(language, TTS_VOICES["hi"])

            synthesis_input = tts.SynthesisInput(text=text)

            voice = tts.VoiceSelectionParams(
                language_code=lang_code,
                name=voice_config["name"],
            )

            audio_config = tts.AudioConfig(
                audio_encoding=tts.AudioEncoding.MP3,
                speaking_rate=speed,
                pitch=0.0,
            )

            response = self._tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )

            audio_base64 = base64.b64encode(response.audio_content).decode("utf-8")
            return audio_base64

        except Exception as e:
            logger.error(f"TTS error: {e}")
            return self._mock_text_to_speech(text, language)

    def _mock_speech_to_text(self, language: str) -> Tuple[str, str, float]:
        """Mock ASR for development."""
        mock_responses = {
            "hi": ("मुझे प्रधानमंत्री किसान योजना के बारे में बताइए", "hi", 0.92),
            "en": ("Tell me about PM Kisan scheme", "en", 0.95),
            "bn": ("প্রধানমন্ত্রী কিষাণ যোজনা সম্পর্কে বলুন", "bn", 0.88),
            "ta": ("பிரதமர் கிசான் திட்டம் பற்றி சொல்லுங்கள்", "ta", 0.85),
            "te": ("ప్రధాన మంత్రి కిసాన్ పథకం గురించి చెప్పండి", "te", 0.86),
            "mr": ("प्रधानमंत्री किसान योजनेबद्दल सांगा", "mr", 0.89),
        }
        return mock_responses.get(language, mock_responses["en"])

    def _mock_text_to_speech(self, text: str, language: str) -> str:
        """Mock TTS for development. Returns a minimal valid base64 audio placeholder."""
        # Return a tiny valid base64 string as placeholder
        placeholder = base64.b64encode(b"MOCK_AUDIO_DATA_" + text[:50].encode()).decode()
        return placeholder

    @property
    def is_live(self) -> bool:
        """Check if using real API or mock."""
        return not self._use_mock


# Singleton
voice_service = VoiceService()
