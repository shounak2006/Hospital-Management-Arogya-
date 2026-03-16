"""
train_all_models.py
Convenience script to train all ML models in sequence.

Run from project root:
  python train_all_models.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print(" MediFind AI – ML Model Training")
print("=" * 60)

print("\n[1/3] Training Sentiment Model …")
from backend.ml_models.sentiment_model import SentimentModel
SentimentModel().train()

print("\n[2/3] Training Trust Score Model …")
from backend.ml_models.trust_score_model import TrustScoreModel
TrustScoreModel().train()

print("\n[3/3] Training Availability + Waiting Time Models …")
from backend.ml_models.availability_model import AvailabilityModel
AvailabilityModel().train()

from backend.ml_models.waiting_time_model import WaitingTimeModel
WaitingTimeModel().train()

print("\n✅ All models trained and saved to backend/models/")
