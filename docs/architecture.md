# JanSahay AI - System Architecture

## Overview
JanSahay AI is a voice-first multilingual AI assistant for government scheme access in India, built as a microservices architecture deployed on AWS.

## Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        WEB["🌐 React Web App"]
        MOB["📱 Mobile App (Android)"]
        WA["💬 WhatsApp Bot"]
    end

    subgraph "API Layer"
        NGX["🔀 Nginx Load Balancer<br/>Rate Limiting | SSL | GZip"]
        GW["🚪 FastAPI API Gateway<br/>OAuth 2.0 | CORS | Compression"]
    end

    subgraph "Core AI Services"
        NLP["🧠 NLP Intent Engine<br/>Intent Detection | Entity Extraction<br/>Context Memory | Language Detection"]
        VOC["🎤 Voice Service<br/>ASR (Speech→Text) | TTS (Text→Speech)<br/>Indian Accent Optimization"]
        REC["🎯 Recommendation Engine<br/>Profile Scoring | TF-IDF Similarity<br/>Popularity Boosting"]
        ELG["✅ Eligibility Engine<br/>Rule-based | AI Hybrid<br/>Multi-criteria Matching"]
        DOC["📋 Document Guidance<br/>10+ Document Types | How-to-Obtain<br/>Multilingual Explanations"]
        LNG["🌐 Language Service<br/>6 Indian Languages<br/>Unicode Detection | i18n"]
    end

    subgraph "Data Layer"
        PG["🐘 PostgreSQL<br/>Users | Schemes | Analytics<br/>Eligibility Rules"]
        RD["⚡ Redis Cache<br/>Query Cache | Session Store<br/>Rate Limit Counters"]
        S3["📦 AWS S3<br/>Assets | Audio Files<br/>Document Templates"]
    end

    subgraph "External APIs"
        GCS["☁️ Google Cloud Speech<br/>ASR | TTS"]
        TWL["📱 Twilio<br/>WhatsApp API"]
        GOV["🏛️ Government APIs<br/>myScheme | DigiLocker"]
    end

    subgraph "Monitoring & DevOps"
        PRM["📊 Prometheus<br/>Metrics Collection"]
        GRF["📈 Grafana<br/>Dashboards | Alerts"]
        GHA["🔄 GitHub Actions<br/>CI/CD Pipeline"]
        ECR["📦 AWS ECR<br/>Docker Registry"]
        ECS["🚀 AWS ECS Fargate<br/>Container Orchestration"]
    end

    WEB --> NGX
    MOB --> NGX
    WA --> NGX
    NGX --> GW

    GW --> NLP
    GW --> VOC
    GW --> REC
    GW --> ELG
    GW --> DOC
    GW --> LNG

    NLP --> PG
    NLP --> RD
    REC --> PG
    ELG --> PG
    VOC --> GCS
    GW --> TWL
    DOC --> PG

    GW --> PG
    GW --> RD
    GW --> S3

    GW --> PRM
    PRM --> GRF
    GHA --> ECR
    ECR --> ECS
```

## Request Flow

```mermaid
sequenceDiagram
    participant U as User
    participant N as Nginx
    participant A as FastAPI
    participant NLP as NLP Engine
    participant R as Recommender
    participant E as Eligibility
    participant DB as PostgreSQL
    participant C as Redis

    U->>N: POST /api/v1/chat/message
    N->>A: Forward (rate limit OK)
    A->>C: Check cache
    C-->>A: Cache miss
    A->>NLP: process_text(message)
    NLP-->>A: Intent + Entities
    A->>R: recommend(profile, schemes)
    R->>DB: Query schemes
    DB-->>R: Scheme data
    R-->>A: Ranked schemes
    A->>E: check_eligibility(profile, scheme)
    E-->>A: Eligibility result
    A->>C: Cache result
    A-->>N: JSON response (GZipped)
    N-->>U: Response
```

## Service Responsibilities

| Service | Technology | Purpose |
|---------|-----------|---------|
| API Gateway | FastAPI + Uvicorn | Routing, auth, middleware |
| NLP Engine | Python (regex + patterns) | Intent detection, entity extraction |
| Voice Service | Google Cloud Speech API | ASR, TTS, Indian accent support |
| Recommender | TF-IDF + weighted scoring | Scheme ranking by profile match |
| Eligibility | Rule engine + fuzzy logic | Multi-criteria eligibility checks |
| Documents | Static + dynamic lookup | Document guidance & how-to-obtain |
| Language Service | Unicode detection + i18n | 6 Indian language support |

## Data Flow
1. **User input** → Voice (ASR) or Text
2. **Language detection** → Unicode script analysis
3. **NLP processing** → Intent + entity extraction
4. **Context merge** → Session memory enrichment
5. **Service routing** → Based on detected intent
6. **Response generation** → Localized text + optional audio (TTS)
7. **Caching** → Redis TTL-based caching for repeat queries
