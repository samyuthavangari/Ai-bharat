"""
JanSahay AI - WhatsApp Bot Integration Service
Handles incoming/outgoing WhatsApp messages via Twilio API.
"""

import logging
from typing import Optional
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class WhatsAppService:
    """WhatsApp Bot Integration using Twilio API."""

    def __init__(self):
        self._client = None
        self._use_mock = settings.TWILIO_ACCOUNT_SID is None

        if not self._use_mock:
            try:
                from twilio.rest import Client
                self._client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                logger.info("Twilio WhatsApp client initialized")
            except ImportError:
                logger.warning("Twilio library not installed. Using mock mode.")
                self._use_mock = True
            except Exception as e:
                logger.warning(f"Failed to init Twilio: {e}. Using mock mode.")
                self._use_mock = True

    async def send_message(self, to: str, body: str) -> Optional[str]:
        """
        Send a WhatsApp message.

        Args:
            to: Recipient phone number (E.164 format)
            body: Message text

        Returns:
            Message SID if successful
        """
        if self._use_mock:
            logger.info(f"[MOCK] WhatsApp to {to}: {body[:100]}...")
            return "MOCK_SID_" + to[-4:]

        try:
            message = self._client.messages.create(
                from_=f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}",
                to=f"whatsapp:{to}",
                body=body,
            )
            logger.info(f"WhatsApp sent to {to}: SID={message.sid}")
            return message.sid
        except Exception as e:
            logger.error(f"WhatsApp send error: {e}")
            return None

    async def process_incoming(self, from_number: str, body: str) -> str:
        """
        Process an incoming WhatsApp message and generate a response.
        This is called by the webhook endpoint.

        Args:
            from_number: Sender's phone number
            body: Message text

        Returns:
            Response text to send back
        """
        from app.services.nlp_engine import process_text
        from app.services.language_service import get_response

        # Process through NLP pipeline
        nlp_result = process_text(
            text=body,
            session_id=f"whatsapp_{from_number}",
        )

        lang = nlp_result.language_detected

        # Generate response based on intent
        from app.schemas import IntentType

        if nlp_result.intent == IntentType.GREETING:
            return get_response("greeting", lang)
        elif nlp_result.intent == IntentType.SCHEME_DISCOVERY:
            return get_response("ask_more_info", lang)
        elif nlp_result.intent == IntentType.ELIGIBILITY_CHECK:
            return get_response("ask_more_info", lang)
        elif nlp_result.intent == IntentType.DOCUMENT_REQUIREMENT:
            return get_response("ask_more_info", lang)
        elif nlp_result.intent == IntentType.APPLICATION_GUIDANCE:
            return get_response("ask_more_info", lang)
        else:
            return get_response("greeting", lang)

    @property
    def is_live(self) -> bool:
        return not self._use_mock


# Singleton
whatsapp_service = WhatsAppService()
