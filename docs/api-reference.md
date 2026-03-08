# JanSahay AI - API Reference

Base URL: `https://api.jansahay.ai/api/v1`

## Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/register` | Register new citizen |
| POST | `/users/login` | Login (returns JWT) |
| GET | `/users/profile` | Get profile (🔒 Auth) |
| PUT | `/users/profile` | Update demographics (🔒 Auth) |

## Schemes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/schemes/?query=&state=&benefit_type=&page=1` | Search/list schemes |
| GET | `/schemes/{scheme_code}?language=en` | Get scheme details |
| GET | `/schemes/recommend/for-me?age=&gender=&state=&income=` | AI recommendations |

## Eligibility
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/eligibility/check?language=en` | Check single scheme |
| POST | `/eligibility/bulk-check?language=en` | Check all schemes |

## Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat/message` | Send text message |
| GET | `/chat/session/{session_id}` | Get session context |

## Voice
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/voice/process` | Full ASR→NLP→TTS pipeline |
| POST | `/voice/tts?text=&language=hi` | Text-to-speech only |
| GET | `/voice/status` | Service status |

## Documents
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/documents/scheme/{scheme_code}?language=en` | Scheme documents |
| GET | `/documents/info/{doc_id}?language=en` | Document details |
| GET | `/documents/search?query=aadhaar` | Search documents |

## Analytics (Admin)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/summary` | Usage summary |
| GET | `/analytics/schemes/popular` | Popular schemes |
| GET | `/analytics/languages` | Language distribution |
| GET | `/analytics/platforms` | Platform distribution |
| GET | `/analytics/states` | State-wise usage |
| GET | `/analytics/trends` | Daily trends |
| GET | `/analytics/dashboard` | Full dashboard data |

## WhatsApp
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/whatsapp/webhook` | Twilio webhook |
| GET | `/whatsapp/status` | Service status |

## Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/languages` | Supported languages |

## Common Query Parameters
- `language` — Language code: `en`, `hi`, `bn`, `ta`, `te`, `mr`
- `page` / `page_size` — Pagination
- All responses follow: `{ success: bool, message: str, data: any }`
