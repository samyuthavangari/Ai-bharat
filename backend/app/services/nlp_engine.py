"""
JanSahay AI - NLP Intent Engine
Detects user intent (scheme discovery, eligibility check, document requirement, application guidance)
and extracts entities (age, income, gender, state, caste category, occupation).
Maintains context memory for multi-turn conversation flow.
"""

import re
import uuid
from typing import Dict, List, Optional, Tuple
from app.schemas import IntentType, NLPResult

# =============================================================================
# Intent Patterns (Multilingual keyword-based classification)
# =============================================================================

INTENT_PATTERNS: Dict[IntentType, Dict[str, List[str]]] = {
    IntentType.SCHEME_DISCOVERY: {
        "en": ["scheme", "yojana", "program", "benefit", "subsidy", "help", "support",
               "government", "welfare", "find scheme", "search", "what schemes",
               "available", "show me", "list", "recommend"],
        "hi": ["योजना", "स्कीम", "लाभ", "सब्सिडी", "सहायता", "सरकारी", "कल्याण",
               "खोजें", "दिखाओ", "कौन सी", "बताओ", "मिलेगा", "सुविधा"],
        "bn": ["প্রকল্প", "যোজনা", "সুবিধা", "ভর্তুকি", "সাহায্য", "সরকারি"],
        "ta": ["திட்டம்", "யோஜனா", "உதவி", "மானியம்", "அரசு"],
        "te": ["పథకం", "యోజన", "సహాయం", "సబ్సిడీ", "ప్రభుత్వ"],
        "mr": ["योजना", "स्कीम", "लाभ", "अनुदान", "मदत", "सरकारी"],
    },
    IntentType.ELIGIBILITY_CHECK: {
        "en": ["eligible", "eligibility", "qualify", "can i get", "am i eligible",
               "do i qualify", "check eligibility", "criteria", "requirement",
               "who can apply", "can i apply"],
        "hi": ["पात्रता", "पात्र", "योग्य", "मिल सकता", "क्या मुझे मिलेगा",
               "जांचें", "शर्तें", "कौन आवेदन कर सकता"],
        "bn": ["যোগ্যতা", "যোগ্য", "পাওয়া যাবে", "আবেদন করতে পারি"],
        "ta": ["தகுதி", "தகுதியானவர்", "விண்ணப்பம்"],
        "te": ["అర్హత", "అర్హులు", "దరఖాస్తు"],
        "mr": ["पात्रता", "पात्र", "अर्ज करू शकतो"],
    },
    IntentType.DOCUMENT_REQUIREMENT: {
        "en": ["document", "documents", "paper", "papers", "what documents",
               "required documents", "paperwork", "id proof", "aadhaar",
               "pan card", "ration card", "certificate"],
        "hi": ["दस्तावेज", "कागजात", "कागज", "डॉक्यूमेंट", "पेपर", "आधार",
               "पैन कार्ड", "राशन कार्ड", "प्रमाण पत्र", "जरूरी कागजात"],
        "bn": ["নথি", "কাগজপত্র", "ডকুমেন্ট", "আধার"],
        "ta": ["ஆவணம்", "ஆவணங்கள்", "ஆதார்", "சான்றிதழ்"],
        "te": ["పత్రాలు", "డాక్యుమెంట్లు", "ఆధార్", "సర్టిఫికేట్"],
        "mr": ["कागदपत्रे", "दस्तऐवज", "आधार", "प्रमाणपत्र"],
    },
    IntentType.APPLICATION_GUIDANCE: {
        "en": ["how to apply", "apply", "application", "apply online", "step by step",
               "process", "procedure", "where to apply", "registration", "form",
               "how to register", "sign up"],
        "hi": ["आवेदन", "अप्लाई", "कैसे करें", "प्रक्रिया", "रजिस्ट्रेशन",
               "फॉर्म", "कहां आवेदन", "ऑनलाइन", "कदम"],
        "bn": ["আবেদন", "কিভাবে", "প্রক্রিয়া", "নিবন্ধন", "ফর্ম"],
        "ta": ["விண்ணப்பம்", "எப்படி", "பதிவு", "படிவம்"],
        "te": ["దరఖాస్తు", "ఎలా", "నమోదు", "ఫారం"],
        "mr": ["अर्ज", "कसे करावे", "प्रक्रिया", "नोंदणी", "फॉर्म"],
    },
    IntentType.GREETING: {
        "en": ["hello", "hi", "hey", "good morning", "good afternoon", "namaste",
               "help", "start", "namaskar"],
        "hi": ["नमस्ते", "नमस्कार", "हैलो", "शुरू", "मदद"],
        "bn": ["নমস্কার", "হ্যালো", "শুরু", "সাহায্য"],
        "ta": ["வணக்கம்", "ஹலோ", "தொடங்கு"],
        "te": ["నమస్కారం", "హలో", "ప్రారంభం"],
        "mr": ["नमस्कार", "हॅलो", "सुरू", "मदत"],
    },
}

# =============================================================================
# Entity Extraction Patterns
# =============================================================================

INDIAN_STATES = [
    "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh",
    "goa", "gujarat", "haryana", "himachal pradesh", "jharkhand", "karnataka",
    "kerala", "madhya pradesh", "maharashtra", "manipur", "meghalaya", "mizoram",
    "nagaland", "odisha", "punjab", "rajasthan", "sikkim", "tamil nadu",
    "telangana", "tripura", "uttar pradesh", "uttarakhand", "west bengal",
    "delhi", "jammu and kashmir", "ladakh", "chandigarh", "puducherry",
    "up", "mp", "hp", "ap", "tn", "wb", "jk"
]

STATE_ABBREVIATIONS = {
    "up": "Uttar Pradesh", "mp": "Madhya Pradesh", "hp": "Himachal Pradesh",
    "ap": "Andhra Pradesh", "tn": "Tamil Nadu", "wb": "West Bengal",
    "jk": "Jammu and Kashmir", "uk": "Uttarakhand",
}

OCCUPATIONS = [
    "farmer", "student", "teacher", "labourer", "worker", "business",
    "self-employed", "unemployed", "artisan", "fisherman", "weaver",
    "kisan", "mazdoor", "vyapari", "kisaan"
]

CASTE_KEYWORDS = {
    "general": ["general", "gen", "सामान्य"],
    "obc": ["obc", "other backward", "अन्य पिछड़ा", "ओबीसी"],
    "sc": ["sc", "scheduled caste", "dalit", "अनुसूचित जाति", "एससी"],
    "st": ["st", "scheduled tribe", "tribal", "adivasi", "अनुसूचित जनजाति", "एसटी"],
    "ews": ["ews", "economically weaker", "आर्थिक रूप से कमजोर"],
}


# =============================================================================
# Conversation Session Store (in-memory, swap to Redis in production)
# =============================================================================
_conversation_sessions: Dict[str, dict] = {}


def get_session(session_id: str) -> dict:
    if session_id not in _conversation_sessions:
        _conversation_sessions[session_id] = {
            "id": session_id,
            "history": [],
            "entities": {},
            "last_intent": None,
            "turn_count": 0,
        }
    return _conversation_sessions[session_id]


def update_session(session_id: str, intent: IntentType, entities: dict):
    session = get_session(session_id)
    session["last_intent"] = intent
    session["turn_count"] += 1
    # Merge entities (keep previous values if not overridden)
    for key, value in entities.items():
        if value is not None:
            session["entities"][key] = value
    # Keep last 20 turns
    session["history"] = session["history"][-20:]


# =============================================================================
# Intent Detection
# =============================================================================

def detect_intent(text: str, language: str = "en") -> Tuple[IntentType, float]:
    """
    Detect user intent from text using keyword matching with confidence scoring.
    Returns (intent, confidence_score).
    """
    text_lower = text.lower().strip()
    scores: Dict[IntentType, float] = {}

    for intent, lang_patterns in INTENT_PATTERNS.items():
        score = 0.0
        # Check all languages for robustness (code-mixing is common)
        for lang, keywords in lang_patterns.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    # Exact match gets higher score
                    if keyword.lower() == text_lower:
                        score += 2.0
                    else:
                        score += 1.0
        scores[intent] = score

    if not scores or max(scores.values()) == 0:
        return IntentType.GENERAL_QUERY, 0.3

    best_intent = max(scores, key=scores.get)
    max_score = scores[best_intent]
    total_score = sum(scores.values()) or 1
    confidence = min(max_score / total_score, 1.0)

    return best_intent, round(confidence, 2)


# =============================================================================
# Entity Extraction
# =============================================================================

def extract_entities(text: str) -> dict:
    """
    Extract structured entities from user text:
    age, income, gender, state, caste_category, occupation.
    """
    text_lower = text.lower()
    entities = {}

    # --- Age ---
    age_patterns = [
        r'(?:age|umra|umar|उम्र|आयु)\s*(?:is|hai|:)?\s*(\d{1,3})',
        r'(\d{1,3})\s*(?:years?\s*old|sal|साल|वर्ष)',
        r'i\s*am\s*(\d{1,3})',
        r'मेरी\s*(?:उम्र|आयु)\s*(\d{1,3})',
    ]
    for pattern in age_patterns:
        match = re.search(pattern, text_lower)
        if match:
            age = int(match.group(1))
            if 1 <= age <= 120:
                entities["age"] = age
                break

    # --- Income ---
    income_patterns = [
        r'(?:income|salary|kamai|आय|कमाई|आमदनी)\s*(?:is|hai|:)?\s*(?:rs\.?|₹|inr)?\s*([\d,]+(?:\.\d+)?)\s*(?:lakh|lac|लाख)?',
        r'(?:rs\.?|₹|inr)\s*([\d,]+(?:\.\d+)?)\s*(?:per\s*(?:year|month|annum))?',
        r'([\d,]+(?:\.\d+)?)\s*(?:lakh|lac|लाख)\s*(?:per\s*(?:year|annum))?',
    ]
    for pattern in income_patterns:
        match = re.search(pattern, text_lower)
        if match:
            income_str = match.group(1).replace(",", "")
            income = float(income_str)
            # If "lakh" mentioned, multiply
            if "lakh" in text_lower or "lac" in text_lower or "लाख" in text_lower:
                income *= 100000
            elif income < 1000:
                income *= 100000  # Assume lakhs if small number with income context
            entities["annual_income"] = income
            break

    # --- Gender ---
    male_keywords = ["male", "man", "boy", "पुरुष", "लड़का", "आदमी", "পুরুষ"]
    female_keywords = ["female", "woman", "girl", "महिला", "लड़की", "औरत", "স্ত্রী", "মহিলা"]
    for kw in female_keywords:
        if kw in text_lower:
            entities["gender"] = "female"
            break
    if "gender" not in entities:
        for kw in male_keywords:
            if kw in text_lower:
                entities["gender"] = "male"
                break

    # --- State ---
    for state in INDIAN_STATES:
        if state in text_lower:
            entities["state"] = STATE_ABBREVIATIONS.get(state, state.title())
            break

    # --- Caste Category ---
    for category, keywords in CASTE_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                entities["caste_category"] = category
                break

    # --- Occupation ---
    for occ in OCCUPATIONS:
        if occ in text_lower:
            entities["occupation"] = occ
            break

    # --- BPL ---
    bpl_keywords = ["bpl", "below poverty", "गरीबी रेखा", "बीपीएल"]
    for kw in bpl_keywords:
        if kw in text_lower:
            entities["is_bpl"] = True
            break

    # --- Farmer ---
    farmer_keywords = ["farmer", "kisan", "किसान", "খামার", "விவசாயி", "రైతు", "शेतकरी"]
    for kw in farmer_keywords:
        if kw in text_lower:
            entities["is_farmer"] = True
            entities["occupation"] = "farmer"
            break

    return entities


# =============================================================================
# Language Detection
# =============================================================================

LANG_CHAR_RANGES = {
    "hi": r'[\u0900-\u097F]',  # Devanagari
    "bn": r'[\u0980-\u09FF]',  # Bengali
    "ta": r'[\u0B80-\u0BFF]',  # Tamil
    "te": r'[\u0C00-\u0C7F]',  # Telugu
    "mr": r'[\u0900-\u097F]',  # Marathi (also Devanagari)
}


def detect_language(text: str) -> str:
    """Detect language from text using Unicode script detection."""
    # Count script occurrences
    script_counts = {}
    for lang, pattern in LANG_CHAR_RANGES.items():
        count = len(re.findall(pattern, text))
        if count > 0:
            script_counts[lang] = count

    if not script_counts:
        return "en"

    # Devanagari could be Hindi or Marathi
    dominant = max(script_counts, key=script_counts.get)

    # Marathi-specific words to disambiguate
    if dominant in ("hi", "mr"):
        marathi_markers = ["आहे", "करा", "नाही", "होते", "करतो", "शेतकरी"]
        for marker in marathi_markers:
            if marker in text:
                return "mr"
        return "hi"

    return dominant


# =============================================================================
# Main NLP Pipeline
# =============================================================================

def process_text(
    text: str,
    session_id: Optional[str] = None,
    language: Optional[str] = None,
) -> NLPResult:
    """
    Full NLP pipeline: language detection → intent classification → entity extraction.
    Maintains conversation context via session_id.
    """
    if not session_id:
        session_id = str(uuid.uuid4())

    # Detect language if not provided
    detected_lang = language or detect_language(text)

    # Detect intent
    intent, confidence = detect_intent(text, detected_lang)

    # Extract entities
    entities = extract_entities(text)

    # Update session context
    update_session(session_id, intent, entities)

    # Merge with session entities for context memory
    session = get_session(session_id)
    merged_entities = {**session["entities"], **entities}

    return NLPResult(
        intent=intent,
        confidence=confidence,
        entities=merged_entities,
        language_detected=detected_lang,
    )
