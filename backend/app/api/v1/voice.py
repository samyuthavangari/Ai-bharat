"""
JanSahay AI - Voice API Routes
Speech-to-text and text-to-speech endpoints for voice-first interaction.
"""

import uuid
from fastapi import APIRouter
from app.schemas import APIResponse, VoiceInput
from app.services.voice_service import voice_service
from app.services.nlp_engine import process_text
from app.services.language_service import get_response
from app.services.recommendation import scheme_recommender
from app.seed.schemes_data import SCHEMES_SEED_DATA

router = APIRouter(prefix="/voice", tags=["Voice"])


@router.post("/process", response_model=APIResponse)
async def process_voice(data: VoiceInput):
    """
    Full voice pipeline:
    1. ASR: Speech → Text
    2. NLP: Text → Intent + Entities
    3. Process: Generate response
    4. TTS: Response → Speech
    Returns both text and audio response.
    """
    session_id = data.session_id or str(uuid.uuid4())

    # Step 1: ASR
    transcribed, detected_lang, asr_confidence = await voice_service.speech_to_text(
        audio_base64=data.audio_base64,
        language=data.language or "hi",
        audio_format=data.format,
    )

    if not transcribed:
        return APIResponse(
            success=False,
            message="Could not transcribe audio. Please try again or type your question.",
            data={"session_id": session_id, "fallback_to_text": True},
        )

    # Step 2: NLP Processing
    nlp_result = process_text(
        text=transcribed,
        session_id=session_id,
        language=detected_lang,
    )

    # Step 3: Generate response text
    lang = nlp_result.language_detected
    from app.schemas import IntentType

    if nlp_result.intent == IntentType.GREETING:
        reply_text = get_response("greeting", lang)
    elif nlp_result.intent == IntentType.SCHEME_DISCOVERY:
        recs = scheme_recommender.recommend(
            user_profile=nlp_result.entities,
            schemes=SCHEMES_SEED_DATA,
            query_text=transcribed,
            top_k=3,
        )
        if recs:
            lang_key = f"name_{lang}"
            names = [r.get(lang_key) or r["name_en"] for r in recs[:3]]
            reply_text = get_response("scheme_found", lang, count=len(names))
            reply_text += "\n" + "\n".join(f"• {n}" for n in names)
        else:
            reply_text = get_response("no_scheme_found", lang)
    else:
        reply_text = get_response("ask_more_info", lang)

    # Step 4: TTS
    reply_audio = await voice_service.text_to_speech(reply_text, lang)

    return APIResponse(
        success=True,
        message="Voice processed",
        data={
            "session_id": session_id,
            "transcribed_text": transcribed,
            "asr_confidence": asr_confidence,
            "language": lang,
            "intent": nlp_result.intent.value,
            "entities": nlp_result.entities,
            "reply_text": reply_text,
            "reply_audio_base64": reply_audio,
        },
    )


@router.post("/tts", response_model=APIResponse)
async def text_to_speech(text: str, language: str = "hi", speed: float = 1.0):
    """Convert text to speech audio."""
    audio = await voice_service.text_to_speech(text, language, speed)
    return APIResponse(
        success=True,
        message="Audio generated",
        data={"audio_base64": audio, "language": language},
    )


@router.get("/status", response_model=APIResponse)
async def voice_service_status():
    """Check voice service status (live API vs mock mode)."""
    return APIResponse(
        success=True,
        message="Voice service status",
        data={
            "is_live": voice_service.is_live,
            "mode": "Google Cloud Speech" if voice_service.is_live else "Mock (development)",
            "supported_languages": ["en", "hi", "bn", "ta", "te", "mr"],
        },
    )
