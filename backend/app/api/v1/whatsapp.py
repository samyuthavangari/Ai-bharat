"""
JanSahay AI - WhatsApp Webhook API Routes
Handles incoming WhatsApp messages via Twilio webhook.
"""

from fastapi import APIRouter, Request, Response
from app.schemas import APIResponse
from app.services.whatsapp_service import whatsapp_service

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])


@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    Twilio WhatsApp webhook endpoint.
    Receives incoming messages and sends back responses.
    """
    form = await request.form()
    from_number = form.get("From", "").replace("whatsapp:", "")
    body = form.get("Body", "")

    if not body:
        return Response(content="OK", status_code=200)

    # Process message
    reply = await whatsapp_service.process_incoming(from_number, body)

    # Send reply
    await whatsapp_service.send_message(from_number, reply)

    # Return TwiML response
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Message>{reply[:1600]}</Message>
    </Response>"""

    return Response(content=twiml, media_type="application/xml")


@router.get("/status", response_model=APIResponse)
async def whatsapp_status():
    """Check WhatsApp service status."""
    return APIResponse(
        success=True,
        message="WhatsApp service status",
        data={
            "is_live": whatsapp_service.is_live,
            "mode": "Twilio API" if whatsapp_service.is_live else "Mock (development)",
        },
    )
