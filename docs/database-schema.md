# JanSahay AI - Database Schema Design

## ER Diagram

```mermaid
erDiagram
    USERS ||--o{ ANALYTICS_EVENTS : generates
    SCHEMES ||--o{ ANALYTICS_EVENTS : referenced_in

    USERS {
        int id PK
        varchar phone_number UK
        varchar email UK
        varchar full_name
        varchar password_hash
        int age
        enum gender "male|female|other"
        varchar state
        varchar district
        enum caste_category "general|obc|sc|st|ews"
        float annual_income
        varchar occupation
        boolean is_rural
        boolean is_bpl
        boolean is_farmer
        boolean is_student
        boolean is_differently_abled
        boolean is_widow
        boolean is_senior_citizen
        int num_children
        enum role "citizen|admin|gov_official"
        varchar preferred_language
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    SCHEMES {
        int id PK
        varchar scheme_code UK
        varchar name_en
        varchar name_hi
        varchar name_bn
        varchar name_ta
        varchar name_te
        varchar name_mr
        text description_en
        text description_hi
        varchar ministry
        varchar department
        varchar scheme_type "central|state"
        varchar target_state
        varchar benefit_type "cash|subsidy|loan|insurance|pension|service"
        varchar benefit_amount
        varchar application_url
        json eligibility_rules
        json required_documents
        json application_steps
        json search_keywords
        float popularity_score
        int total_searches
        boolean is_active
        timestamp created_at
    }

    ANALYTICS_EVENTS {
        int id PK
        int user_id FK
        varchar event_type "scheme_search|eligibility_check|voice_query"
        int scheme_id FK
        varchar language
        varchar platform "web|mobile|whatsapp"
        varchar query_text
        varchar intent_detected
        varchar is_eligible "yes|no|partial"
        varchar session_id
        float response_time_ms
        json metadata
        timestamp created_at
    }
```

## Table Details

### `users` — 23 columns
Stores citizen profiles with demographic data crucial for scheme matching.

### `schemes` — 25 columns
Government scheme database with multilingual metadata, JSON eligibility rules, and required documents.

### `analytics_events` — 13 columns
Event tracking for searches, eligibility checks, voice queries, and platform usage.

## Indexes
- `users.phone_number` — Unique, for login
- `users.email` — Unique, for login
- `schemes.scheme_code` — Unique, for lookups
- `analytics_events.event_type` — For dashboard queries
- `analytics_events.created_at` — For time-range queries
