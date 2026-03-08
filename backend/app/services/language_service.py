"""
JanSahay AI - Language Service
Language detection, translation helpers, and multilingual response generation.
Supports: English, Hindi, Bengali, Tamil, Telugu, Marathi.
"""

from typing import Dict, Optional


# =============================================================================
# Multilingual Response Templates
# =============================================================================

RESPONSE_TEMPLATES: Dict[str, Dict[str, str]] = {
    "greeting": {
        "en": "🙏 Namaste! Welcome to JanSahay AI. I can help you find government schemes, check eligibility, and guide you through applications. How can I help you today?",
        "hi": "🙏 नमस्ते! JanSahay AI में आपका स्वागत है। मैं सरकारी योजनाएं खोजने, पात्रता जांचने और आवेदन प्रक्रिया में आपकी मदद कर सकता हूं। आज मैं आपकी कैसे मदद कर सकता हूं?",
        "bn": "🙏 নমস্কার! JanSahay AI-তে আপনাকে স্বাগতম। আমি সরকারি প্রকল্প খুঁজতে, যোগ্যতা যাচাই করতে এবং আবেদন প্রক্রিয়ায় সাহায্য করতে পারি।",
        "ta": "🙏 வணக்கம்! JanSahay AI-க்கு வரவேற்கிறோம். அரசு திட்டங்களைக் கண்டறிய, தகுதியை சரிபார்க்க மற்றும் விண்ணப்ப செயல்முறையில் உங்களுக்கு உதவ முடியும்.",
        "te": "🙏 నమస్కారం! JanSahay AI కి స్వాగతం. ప్రభుత్వ పథకాలను కనుగొనడం, అర్హతను తనిఖీ చేయడం మరియు దరఖాస్తు ప్రక్రియలో మీకు సహాయం చేయగలను.",
        "mr": "🙏 नमस्कार! JanSahay AI मध्ये आपले स्वागत आहे. मी सरकारी योजना शोधणे, पात्रता तपासणे आणि अर्ज प्रक्रियेत मदत करू शकतो.",
    },
    "scheme_found": {
        "en": "I found {count} schemes that may be relevant to you:",
        "hi": "मुझे {count} योजनाएं मिलीं जो आपके लिए उपयुक्त हो सकती हैं:",
        "bn": "আমি {count}টি প্রকল্প পেয়েছি যা আপনার জন্য প্রাসঙ্গিক হতে পারে:",
        "ta": "{count} திட்டங்கள் உங்களுக்குப் பொருத்தமானவை:",
        "te": "మీకు సంబంధించిన {count} పథకాలు కనుగొనబడ్డాయి:",
        "mr": "तुमच्यासाठी {count} योजना सापडल्या:",
    },
    "no_scheme_found": {
        "en": "I couldn't find any matching schemes. Try providing more details about yourself (age, state, occupation, income).",
        "hi": "मुझे कोई मेल खाती योजना नहीं मिली। अपने बारे में अधिक जानकारी दें (उम्र, राज्य, व्यवसाय, आय)।",
        "bn": "কোনো মিলিত প্রকল্প পাওয়া যায়নি। আপনার সম্পর্কে আরও তথ্য দিন।",
        "ta": "எந்தத் திட்டமும் கிடைக்கவில்லை. உங்கள் விவரங்களைக் கொடுங்கள்.",
        "te": "ఏ పథకం కనుగొనబడలేదు. మీ వివరాలను అందించండి.",
        "mr": "कोणतीही योजना सापडली नाही. अधिक माहिती द्या.",
    },
    "eligible": {
        "en": "✅ Great news! You appear to be eligible for this scheme.",
        "hi": "✅ अच्छी खबर! आप इस योजना के लिए पात्र प्रतीत होते हैं।",
        "bn": "✅ সুখবর! আপনি এই প্রকল্পের জন্য যোগ্য বলে মনে হচ্ছে।",
        "ta": "✅ நல்ல செய்தி! இந்தத் திட்டத்திற்கு நீங்கள் தகுதியானவர்.",
        "te": "✅ శుభవార్త! మీరు ఈ పథకానికి అర్హులుగా కనిపిస్తున్నారు.",
        "mr": "✅ चांगली बातमी! तुम्ही या योजनेसाठी पात्र दिसत आहात.",
    },
    "not_eligible": {
        "en": "❌ Unfortunately, you may not be eligible for this scheme. Here's why:",
        "hi": "❌ दुर्भाग्य से, आप इस योजना के लिए पात्र नहीं हो सकते। कारण:",
        "bn": "❌ দুর্ভাগ্যবশত, আপনি এই প্রকল্পের জন্য যোগ্য নাও হতে পারেন। কারণ:",
        "ta": "❌ துரதிர்ஷ்டவசமாக, இந்தத் திட்டத்திற்கு நீங்கள் தகுதியற்றவராக இருக்கலாம்.",
        "te": "❌ దురదృష్టవశాత్తు, మీరు ఈ పథకానికి అర్హులు కాకపోవచ్చు.",
        "mr": "❌ दुर्दैवाने, तुम्ही या योजनेसाठी पात्र नसू शकता. कारण:",
    },
    "ask_more_info": {
        "en": "To help you better, could you tell me:\n• Your age\n• Your state\n• Your occupation\n• Your annual income",
        "hi": "बेहतर मदद के लिए, कृपया बताएं:\n• आपकी उम्र\n• आपका राज्य\n• आपका व्यवसाय\n• आपकी वार्षिक आय",
        "bn": "আপনাকে আরও ভালোভাবে সাহায্য করতে, অনুগ্রহ করে বলুন:\n• আপনার বয়স\n• আপনার রাজ্য\n• আপনার পেশা\n• আপনার বার্ষিক আয়",
        "ta": "உங்களுக்கு சிறப்பாக உதவ, தயவுசெய்து சொல்லுங்கள்:\n• உங்கள் வயது\n• உங்கள் மாநிலம்\n• உங்கள் தொழில்\n• உங்கள் ஆண்டு வருமானம்",
        "te": "మీకు మెరుగ్గా సహాయం చేయడానికి, దయచేసి చెప్పండి:\n• మీ వయస్సు\n• మీ రాష్ట్రం\n• మీ వృత్తి\n• మీ వార్షిక ఆదాయం",
        "mr": "तुम्हाला अधिक चांगल्या प्रकारे मदत करण्यासाठी, कृपया सांगा:\n• तुमचे वय\n• तुमचे राज्य\n• तुमचा व्यवसाय\n• तुमचे वार्षिक उत्पन्न",
    },
    "documents_intro": {
        "en": "📋 Here are the documents you'll need for this scheme:",
        "hi": "📋 इस योजना के लिए आपको इन दस्तावेजों की आवश्यकता होगी:",
        "bn": "📋 এই প্রকল্পের জন্য আপনার যে নথিগুলি প্রয়োজন:",
        "ta": "📋 இந்தத் திட்டத்திற்குத் தேவையான ஆவணங்கள்:",
        "te": "📋 ఈ పథకానికి మీకు అవసరమైన పత్రాలు:",
        "mr": "📋 या योजनेसाठी आवश्यक कागदपत्रे:",
    },
    "application_steps_intro": {
        "en": "📝 Here's how to apply step by step:",
        "hi": "📝 आवेदन करने के लिए ये कदम उठाएं:",
        "bn": "📝 আবেদন করার পদ্ধতি:",
        "ta": "📝 படிப்படியாக விண்ணப்பிக்கும் வழி:",
        "te": "📝 దశల వారీగా దరఖాస్తు చేయడం ఎలా:",
        "mr": "📝 अर्ज करण्याच्या पायऱ्या:",
    },
    "error": {
        "en": "Sorry, something went wrong. Please try again.",
        "hi": "क्षमा करें, कुछ गलत हो गया। कृपया पुनः प्रयास करें।",
        "bn": "দুঃখিত, কিছু ভুল হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।",
        "ta": "மன்னிக்கவும், ஏதோ தவறு நடந்தது. மீண்டும் முயற்சிக்கவும்.",
        "te": "క్షమించండి, ఏదో తప్పు జరిగింది. దయచేసి మళ్ళీ ప్రయత్నించండి.",
        "mr": "क्षमस्व, काहीतरी चूक झाली. कृपया पुन्हा प्रयत्न करा.",
    },
}

# Language names in their own script
LANGUAGE_NAMES = {
    "en": "English",
    "hi": "हिन्दी",
    "bn": "বাংলা",
    "ta": "தமிழ்",
    "te": "తెలుగు",
    "mr": "मराठी",
}


def get_response(template_key: str, language: str = "en", **kwargs) -> str:
    """Get a localized response template with variable substitution."""
    templates = RESPONSE_TEMPLATES.get(template_key, {})
    text = templates.get(language, templates.get("en", ""))
    if kwargs:
        text = text.format(**kwargs)
    return text


def get_supported_languages() -> Dict[str, str]:
    """Return dict of supported language codes and their native names."""
    return LANGUAGE_NAMES.copy()
