"""
JanSahay AI - Document Guidance Module
Explains required documents, provides simplified explanations,
and suggests how to obtain them in multiple languages.
"""

from typing import Dict, List, Optional


# =============================================================================
# Master Document Library (multilingual)
# =============================================================================

DOCUMENT_LIBRARY: Dict[str, dict] = {
    "aadhaar": {
        "name": {
            "en": "Aadhaar Card",
            "hi": "आधार कार्ड",
            "bn": "আধার কার্ড",
            "ta": "ஆதார் அட்டை",
            "te": "ఆధార్ కార్డ్",
            "mr": "आधार कार्ड",
        },
        "description": {
            "en": "12-digit unique identification number issued by the Unique Identification Authority of India (UIDAI). It serves as proof of identity and address.",
            "hi": "भारतीय विशिष्ट पहचान प्राधिकरण (UIDAI) द्वारा जारी 12 अंकों का विशिष्ट पहचान नंबर। यह पहचान और पते का प्रमाण है।",
        },
        "how_to_obtain": {
            "en": "Visit your nearest Aadhaar Seva Kendra or Post Office. Carry any existing ID proof and address proof. You can also apply online at uidai.gov.in. It is free of charge.",
            "hi": "अपने निकटतम आधार सेवा केंद्र या डाकघर जाएं। कोई भी मौजूदा पहचान पत्र और पते का प्रमाण ले जाएं। आप uidai.gov.in पर ऑनलाइन भी आवेदन कर सकते हैं। यह निःशुल्क है।",
        },
    },
    "ration_card": {
        "name": {
            "en": "Ration Card",
            "hi": "राशन कार्ड",
            "bn": "রেশন কার্ড",
            "ta": "ரேஷன் அட்டை",
            "te": "రేషన్ కార్డ్",
            "mr": "रेशन कार्ड",
        },
        "description": {
            "en": "Government-issued document used for buying subsidized food grains. Also serves as identity and address proof. Types: APL (Above Poverty Line), BPL (Below Poverty Line), AAY (Antyodaya).",
            "hi": "सरकार द्वारा जारी दस्तावेज जो सब्सिडी वाले अनाज खरीदने के लिए उपयोग किया जाता है। यह पहचान और पते के प्रमाण के रूप में भी काम करता है।",
        },
        "how_to_obtain": {
            "en": "Apply at your nearest Food & Civil Supplies Department office or through the state e-governance portal. Required: Aadhaar cards of all family members, address proof, and family income certificate.",
            "hi": "अपने निकटतम खाद्य एवं नागरिक आपूर्ति विभाग कार्यालय में या राज्य ई-गवर्नेंस पोर्टल के माध्यम से आवेदन करें।",
        },
    },
    "income_certificate": {
        "name": {
            "en": "Income Certificate",
            "hi": "आय प्रमाण पत्र",
            "bn": "আয়ের সার্টিফিকেট",
            "ta": "வருமான சான்றிதழ்",
            "te": "ఆదాయ ధృవీకరణ పత్రం",
            "mr": "उत्पन्न प्रमाणपत्र",
        },
        "description": {
            "en": "Certificate issued by the state government confirming your annual family income. Essential for schemes with income-based eligibility.",
            "hi": "राज्य सरकार द्वारा जारी प्रमाण पत्र जो आपकी वार्षिक पारिवारिक आय की पुष्टि करता है।",
        },
        "how_to_obtain": {
            "en": "Apply at your Tehsildar office or Block Development Office. You can also apply online through your state's e-District portal. Required: Aadhaar, ration card, self-declaration of income.",
            "hi": "तहसीलदार कार्यालय या ब्लॉक विकास कार्यालय में आवेदन करें। आप अपने राज्य के ई-डिस्ट्रिक्ट पोर्टल से ऑनलाइन भी आवेदन कर सकते हैं।",
        },
    },
    "caste_certificate": {
        "name": {
            "en": "Caste Certificate",
            "hi": "जाति प्रमाण पत्र",
            "bn": "জাতি সার্টিফিকেট",
            "ta": "சாதி சான்றிதழ்",
            "te": "కుల ధృవీకరణ పత్రం",
            "mr": "जात प्रमाणपत्र",
        },
        "description": {
            "en": "Certificate proving your SC/ST/OBC caste category, issued by the state Revenue Department.",
            "hi": "राज्य राजस्व विभाग द्वारा जारी प्रमाण पत्र जो आपकी SC/ST/OBC जाति श्रेणी को प्रमाणित करता है।",
        },
        "how_to_obtain": {
            "en": "Apply at the Tehsildar or Sub-Divisional Magistrate office. Required: Aadhaar, father's caste certificate (if available), school records, ration card.",
            "hi": "तहसीलदार या उप-विभागीय मजिस्ट्रेट कार्यालय में आवेदन करें।",
        },
    },
    "bank_passbook": {
        "name": {
            "en": "Bank Passbook / Account Details",
            "hi": "बैंक पासबुक / खाता विवरण",
            "bn": "ব্যাংক পাসবুক",
            "ta": "வங்கி பாஸ்புக்",
            "te": "బ్యాంక్ పాస్ బుక్",
            "mr": "बँक पासबुक",
        },
        "description": {
            "en": "Bank account passbook or statement showing your account number, IFSC code, and account holder name. Required for Direct Benefit Transfer (DBT).",
            "hi": "बैंक खाता पासबुक जिसमें खाता संख्या, IFSC कोड, और खाताधारक का नाम दिखाई दे।",
        },
        "how_to_obtain": {
            "en": "Open a Jan Dhan account at any bank branch for free. Carry: Aadhaar card, passport photo, and mobile number.",
            "hi": "किसी भी बैंक शाखा में मुफ्त जन धन खाता खोलें। साथ रखें: आधार कार्ड, पासपोर्ट फोटो, और मोबाइल नंबर।",
        },
    },
    "pan_card": {
        "name": {
            "en": "PAN Card",
            "hi": "पैन कार्ड",
            "bn": "প্যান কার্ড",
            "ta": "பான் அட்டை",
            "te": "పాన్ కార్డ్",
            "mr": "पॅन कार्ड",
        },
        "description": {
            "en": "Permanent Account Number issued by the Income Tax Department. 10-character alphanumeric ID for tax purposes.",
            "hi": "आयकर विभाग द्वारा जारी स्थायी खाता संख्या। कर उद्देश्यों के लिए 10 अक्षरों का अल्फ़ान्यूमेरिक आईडी।",
        },
        "how_to_obtain": {
            "en": "Apply online at incometax.gov.in or nsdl.com. You can also apply through your nearest PAN center. Fee: ₹107.",
            "hi": "incometax.gov.in या nsdl.com पर ऑनलाइन आवेदन करें।",
        },
    },
    "domicile_certificate": {
        "name": {
            "en": "Domicile Certificate",
            "hi": "निवास प्रमाण पत्र",
            "bn": "ডোমিসাইল সার্টিফিকেট",
            "ta": "குடியிருப்பு சான்றிதழ்",
            "te": "నివాస ధృవీకరణ పత్రం",
            "mr": "अधिवास प्रमाणपत्र",
        },
        "description": {
            "en": "Proof that you are a permanent resident of a particular state. Required for state-specific schemes.",
            "hi": "प्रमाण कि आप किसी विशेष राज्य के स्थायी निवासी हैं।",
        },
        "how_to_obtain": {
            "en": "Apply at Tehsildar office or through your state's e-District portal. Required: Aadhaar, voter ID, and utility bills showing residency.",
            "hi": "तहसीलदार कार्यालय या राज्य के ई-डिस्ट्रिक्ट पोर्टल से आवेदन करें।",
        },
    },
    "land_records": {
        "name": {
            "en": "Land Ownership Records (Khatauni/Patta)",
            "hi": "भूमि स्वामित्व रिकॉर्ड (खतौनी/पट्टा)",
        },
        "description": {
            "en": "Official land records proving ownership or tenancy. Required for farmer-specific schemes like PM-KISAN.",
            "hi": "भूमि स्वामित्व या किरायेदारी साबित करने वाले आधिकारिक भूमि रिकॉर्ड।",
        },
        "how_to_obtain": {
            "en": "Access through Bhulekh (UP), Bhoomi (Karnataka), or your state's land records portal. Visit the local Lekhpal/Patwari office for certified copies.",
            "hi": "भूलेख (UP), भूमि (कर्नाटक) या अपने राज्य के भूमि रिकॉर्ड पोर्टल से प्राप्त करें।",
        },
    },
    "voter_id": {
        "name": {
            "en": "Voter ID (EPIC)",
            "hi": "मतदाता पहचान पत्र",
        },
        "description": {
            "en": "Election Photo Identity Card issued by the Election Commission of India.",
            "hi": "भारत के चुनाव आयोग द्वारा जारी चुनाव फोटो पहचान पत्र।",
        },
        "how_to_obtain": {
            "en": "Apply online at voters.eci.gov.in or visit your nearest Electoral Registration Office. Fill Form 6.",
            "hi": "voters.eci.gov.in पर ऑनलाइन आवेदन करें या निकटतम मतदान पंजीकरण कार्यालय जाएं।",
        },
    },
    "disability_certificate": {
        "name": {
            "en": "Disability Certificate",
            "hi": "विकलांगता प्रमाण पत्र",
        },
        "description": {
            "en": "Certificate issued by a government hospital certifying the type and percentage of disability.",
            "hi": "सरकारी अस्पताल द्वारा जारी प्रमाण पत्र जो विकलांगता के प्रकार और प्रतिशत को प्रमाणित करता है।",
        },
        "how_to_obtain": {
            "en": "Visit the nearest government district hospital. A medical board will assess and issue the certificate. Free of charge.",
            "hi": "निकटतम सरकारी जिला अस्पताल जाएं। मेडिकल बोर्ड मूल्यांकन करेगा और प्रमाण पत्र जारी करेगा।",
        },
    },
}


class DocumentGuidanceService:
    """Provides document requirement information and guidance for schemes."""

    def get_scheme_documents(
        self,
        scheme: dict,
        language: str = "en",
    ) -> List[dict]:
        """
        Get required documents for a scheme with localized descriptions.

        Args:
            scheme: Scheme dict containing required_documents list
            language: Language code

        Returns:
            List of document info dicts with name, description, how_to_obtain
        """
        raw_docs = scheme.get("required_documents") or []
        result = []

        for doc in raw_docs:
            doc_id = doc.get("id", "")
            lib_entry = DOCUMENT_LIBRARY.get(doc_id, {})

            # Get localized name
            name = (
                doc.get(f"name_{language}")
                or (lib_entry.get("name", {}).get(language))
                or doc.get("name_en", "")
                or (lib_entry.get("name", {}).get("en", "Unknown Document"))
            )

            # Get localized description
            description = (
                doc.get(f"description_{language}")
                or (lib_entry.get("description", {}).get(language))
                or doc.get("description_en", "")
                or (lib_entry.get("description", {}).get("en", ""))
            )

            # Get how-to-obtain
            how_to = (
                doc.get(f"how_to_obtain_{language}")
                or (lib_entry.get("how_to_obtain", {}).get(language))
                or doc.get("how_to_obtain_en", "")
                or (lib_entry.get("how_to_obtain", {}).get("en", ""))
            )

            result.append({
                "name": name,
                "description": description,
                "how_to_obtain": how_to,
                "is_mandatory": doc.get("is_mandatory", True),
            })

        return result

    def get_document_info(
        self,
        document_id: str,
        language: str = "en",
    ) -> Optional[dict]:
        """Get details for a specific document type."""
        entry = DOCUMENT_LIBRARY.get(document_id)
        if not entry:
            return None

        return {
            "id": document_id,
            "name": entry["name"].get(language, entry["name"].get("en", "")),
            "description": entry.get("description", {}).get(
                language, entry.get("description", {}).get("en", "")
            ),
            "how_to_obtain": entry.get("how_to_obtain", {}).get(
                language, entry.get("how_to_obtain", {}).get("en", "")
            ),
        }

    def search_documents(
        self, query: str, language: str = "en"
    ) -> List[dict]:
        """Search document library by name."""
        query_lower = query.lower()
        results = []
        for doc_id, entry in DOCUMENT_LIBRARY.items():
            # Search across all language names
            for lang, name in entry.get("name", {}).items():
                if query_lower in name.lower() or query_lower in doc_id:
                    results.append(self.get_document_info(doc_id, language))
                    break
        return results


# Singleton
document_guidance = DocumentGuidanceService()
