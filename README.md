# AI-Powered Emergency Hospital Recommendation System

> **MediFind AI** — An intelligent system that finds the best hospital during medical emergencies using ML predictions, NLP sentiment analysis, multi-factor ranking, and real-time crowd data.

---

## 🏗️ Project Structure

```
Hospital management/
├── backend/
│   ├── api/                      # FastAPI route handlers
│   │   ├── hospital_routes.py    # GET /hospitals/nearby, /ranked
│   │   ├── recommendation_routes.py  # GET /hospitals/recommendations
│   │   ├── triage_routes.py      # POST /triage
│   │   ├── report_routes.py      # POST /report, GET /waitingtime
│   │   └── routing.py            # OSM/OSRM navigation
│   ├── ml_models/                # Machine Learning models
│   │   ├── sentiment_model.py    # NLTK + TF-IDF + Logistic Regression
│   │   ├── trust_score_model.py  # Isolation Forest anomaly detection
│   │   ├── triage_classifier.py  # Emergency → specialization mapping
│   │   ├── availability_model.py # Random Forest availability predictor
│   │   ├── waiting_time_model.py # Random Forest waiting time regressor
│   │   └── ranking_engine.py     # Multi-factor hospital scoring
│   ├── data_pipeline/
│   │   ├── synthetic_data_generator.py  # Generates 500 hospitals + 2500 reviews
│   │   ├── hospital_collector.py        # Google Places API integration
│   │   └── review_processor.py         # Batch NLP processing
│   ├── database/
│   │   ├── database.py           # SQLAlchemy engine + sessions
│   │   └── models.py             # Hospital, Review, UserReport, TriageRequest
│   └── main.py                   # FastAPI app entry point
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── EmergencyForm.js      # Emergency input form
│       │   ├── HospitalList.js       # Ranked hospital list
│       │   ├── MapView.js            # Leaflet interactive map
│       │   ├── RecommendationPanel.js # Alternative recommendations
│       │   └── RouteDisplay.js       # Route navigation + ETA
│       ├── App.js                # Main state orchestrator
│       └── index.css             # Premium dark dashboard CSS
├── config/
│   └── weights.yaml              # Configurable ranking weights
├── train_all_models.py           # Train all ML models
├── requirements.txt
└── README.md
```

---

## 🚀 Setup Instructions

### Prerequisites

- **Python 3.10+** (with pip)
- **Node.js 18+** (with npm)
- **PostgreSQL 14+** running locally

---

### Step 1: Create & Activate Python Virtual Environment

```bash
# Open PowerShell in the project folder:
cd "C:\Users\User\Downloads\Hospital management"

# Create virtual environment
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs: FastAPI, SQLAlchemy, scikit-learn, NLTK, pandas, numpy, psycopg2, and others.

---

### Step 3: Create PostgreSQL Database

Open **pgAdmin** or **psql** and run:

```sql
CREATE DATABASE hospital_db;
```

The default credentials in `.env` are:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hospital_db
```

Edit `.env` if your credentials are different.

---

### Step 4: Generate Synthetic Data + Initialize DB

```bash
python -m backend.data_pipeline.synthetic_data_generator
```

This will:
- Create all database tables
- Insert **500 synthetic hospitals** with realistic features
- Insert **2,500 synthetic reviews**

---

### Step 5: Train All ML Models

```bash
python train_all_models.py
```

This trains and saves (to `backend/models/`):
- `sentiment_model.pkl` — NLP review sentiment
- `trust_model.pkl` — Isolation Forest trust detector
- `trust_scaler.pkl` — Feature scaler for trust model
- `availability_model.pkl` — Random Forest availability predictor
- `waiting_time_model.pkl` — Random Forest waiting time regressor

---

### Step 6: Start the Backend Server

```bash
uvicorn backend.main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

### Step 7: Install & Start Frontend

```bash
cd frontend
npm install
npm start
```

The dashboard opens at **http://localhost:3000**

---

## 🌐 API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | System health check |
| `GET` | `/hospitals/nearby` | Hospitals near a location |
| `GET` | `/hospitals/ranked` | Multi-factor ranked hospitals |
| `GET` | `/hospitals/recommendations` | Alternative hospital suggestions |
| `POST` | `/triage` | Emergency classification + ranked hospitals |
| `GET` | `/waitingtime` | Predicted wait time for a hospital |
| `POST` | `/report` | Submit crowd-sourced report |
| `GET` | `/route` | OSM driving route + ETA |

### Example Requests

**Find ranked hospitals:**
```bash
curl "http://localhost:8000/hospitals/ranked?lat=12.97&lng=77.59&radius=15&specializations=cardiac"
```

**Triage emergency:**
```bash
curl -X POST http://localhost:8000/triage \
  -H "Content-Type: application/json" \
  -d "{\"emergency_type\":\"cardiac_arrest\",\"severity\":9,\"patient_age\":55,\"user_lat\":12.97,\"user_lng\":77.59}"
```

**Submit crowd report:**
```bash
curl -X POST http://localhost:8000/report \
  -H "Content-Type: application/json" \
  -d "{\"hospital_id\":1,\"waiting_time\":20,\"queue_length\":8,\"availability\":true}"
```

---

## 🏥 Hospital Ranking Formula

```
HospitalScore =
  w1 × (rating / 5)
+ w2 × sentiment_score
+ w3 × distance_score
+ w4 × specialization_match
+ w5 × affordability_score
+ w6 × availability_probability
+ w7 × (1 - wait_time / 120)
+ w8 × trust_score
```

Default weights (editable in `config/weights.yaml`):
| Weight | Factor | Value |
|--------|--------|-------|
| w1 | Rating | 0.15 |
| w2 | Sentiment | 0.10 |
| w3 | Distance | 0.20 |
| w4 | Specialization Match | 0.20 |
| w5 | Affordability | 0.05 |
| w6 | Availability | 0.15 |
| w7 | Waiting Time | 0.10 |
| w8 | Trust Score | 0.05 |

---

## 🤖 ML Models Summary

| Model | Algorithm | Purpose |
|-------|-----------|---------|
| Sentiment Model | TF-IDF + Logistic Regression | Hospital review NLP scoring |
| Trust Score | Isolation Forest | Fake review detection |
| Triage Classifier | Rule-based + heuristics | Emergency → specializations |
| Availability Predictor | Random Forest Classifier | Hospital capacity probability |
| Waiting Time Predictor | Random Forest Regressor | Expected wait in minutes |

---

## 🔑 Optional: Google Places API

To fetch real hospitals near any location:

1. Get an API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Add it to `.env`: `GOOGLE_PLACES_API_KEY=your_key_here`
3. Run: `python -m backend.data_pipeline.hospital_collector --lat 12.97 --lng 77.59`

The system works fully without this key using the 500 synthetic hospitals.

---

## 🗺️ Map Navigation

The frontend uses **Leaflet.js** with **OpenStreetMap** tiles. Routes are fetched from the **OSRM** public API (no API key required). Falls back to straight-line distance if OSRM is unavailable.

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI app entry point |
| `config/weights.yaml` | Tune hospital ranking weights |
| `.env` | Database URL + API keys |
| `train_all_models.py` | Train all ML models at once |
| `backend/data_pipeline/synthetic_data_generator.py` | Seed database |

---

## 🛠 Troubleshooting

**`ModuleNotFoundError: backend`** → Run commands from the project root (`Hospital management/`)

**PostgreSQL connection error** → Ensure PostgreSQL is running and credentials in `.env` are correct

**CORS errors on frontend** → Ensure backend is running on port 8000 and `CORS_ORIGIN=http://localhost:3000` in `.env`

**NLTK resource missing** → The sentiment model auto-downloads NLTK data on first run. Ensure internet access.

**Execution policy error (PowerShell)** → Run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
