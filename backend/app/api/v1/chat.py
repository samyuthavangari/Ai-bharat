"""
JanSahay AI - Chat API Routes
Text-based conversational interface with NLP intent processing.
"""

import uuid
from fastapi import APIRouter
from app.schemas import APIResponse, ChatMessage, IntentType
from app.services.nlp_engine import process_text, get_session
from app.services.language_service import get_response
from app.services.recommendation import scheme_recommender
from app.services.eligibility import eligibility_engine
from app.services.document_guidance import document_guidance
from app.seed.schemes_data import SCHEMES_SEED_DATA

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/message", response_model=APIResponse)
async def chat_message(data: ChatMessage):
    """
    Process a chat message through the NLP pipeline.
    Detects intent, extracts entities, and generates contextual response.
    """
    session_id = data.session_id or str(uuid.uuid4())

    # Run NLP pipeline
    nlp_result = process_text(
        text=data.text,
        session_id=session_id,
        language=data.language,
    )

    lang = nlp_result.language_detected
    entities = nlp_result.entities
    response_data = {
        "session_id": session_id,
        "intent": nlp_result.intent.value,
        "confidence": nlp_result.confidence,
        "entities": entities,
        "language": lang,
    }

    # Generate response based on intent
    if nlp_result.intent == IntentType.GREETING:
        response_data["reply"] = get_response("greeting", lang)

    elif nlp_result.intent == IntentType.SCHEME_DISCOVERY:
        # Recommend schemes based on extracted entities
        profile = {
            "age": entities.get("age"),
            "gender": entities.get("gender"),
            "state": entities.get("state"),
            "annual_income": entities.get("annual_income"),
            "occupation": entities.get("occupation"),
            "caste_category": entities.get("caste_category"),
            "is_rural": entities.get("is_rural"),
            "is_bpl": entities.get("is_bpl"),
            "is_farmer": entities.get("is_farmer"),
        }

        recommendations = scheme_recommender.recommend(
            user_profile=profile,
            schemes=SCHEMES_SEED_DATA,
            query_text=data.text,
            top_k=5,
        )

        if recommendations:
            lang_key = f"name_{lang}"
            schemes_list = []
            for r in recommendations:
                schemes_list.append({
                    "scheme_code": r["scheme_code"],
                    "name": r.get(lang_key) or r["name_en"],
                    "benefit": r.get("benefit_amount", ""),
                    "score": r["match_score"],
                })

            response_data["reply"] = get_response("scheme_found", lang, count=len(schemes_list))
            response_data["schemes"] = schemes_list
        else:
            response_data["reply"] = get_response("no_scheme_found", lang)

        # Ask for more info if entities are sparse
        if len(entities) < 3:
            response_data["reply"] += "\n\n" + get_response("ask_more_info", lang)

    elif nlp_result.intent == IntentType.ELIGIBILITY_CHECK:
        profile = {k: v for k, v in entities.items()}
        results = eligibility_engine.bulk_check(profile, SCHEMES_SEED_DATA)

        if results["eligible_schemes"]:
            response_data["reply"] = get_response("eligible", lang)
            response_data["eligible_schemes"] = results["eligible_schemes"][:5]
        else:
            response_data["reply"] = get_response("not_eligible", lang)
            response_data["partially_eligible"] = results["partially_eligible"][:5]

        if len(entities) < 3:
            response_data["reply"] += "\n\n" + get_response("ask_more_info", lang)

    elif nlp_result.intent == IntentType.DOCUMENT_REQUIREMENT:
        # Find scheme from context and show required documents
        response_data["reply"] = get_response("documents_intro", lang)
        # Show documents for top recommended scheme
        session = get_session(session_id)
        top_scheme = SCHEMES_SEED_DATA[0]  # default
        docs = document_guidance.get_scheme_documents(top_scheme, lang)
        response_data["documents"] = docs
        response_data["reply"] += "\n\n" + get_response("ask_more_info", lang)

    elif nlp_result.intent == IntentType.APPLICATION_GUIDANCE:
        response_data["reply"] = get_response("application_steps_intro", lang)
        # Show steps for a scheme
        top_scheme = SCHEMES_SEED_DATA[0]
        steps = top_scheme.get("application_steps", [])
        response_data["application_steps"] = steps

    else:
        response_data["reply"] = get_response("greeting", lang)

    return APIResponse(
        success=True,
        message="Message processed",
        data=response_data,
    )


@router.get("/session/{session_id}", response_model=APIResponse)
async def get_chat_session(session_id: str):
    """Get conversation session context (entities collected so far)."""
    session = get_session(session_id)
    return APIResponse(
        success=True,
        message="Session retrieved",
        data=session,
    )
