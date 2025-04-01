import os
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer

DATA_PROCESSED = "data/processed/cleaned_comments.csv"
FEATURES_DIR = "data/processed"
os.makedirs(FEATURES_DIR, exist_ok=True)

def extract_features():
    """Converts cleaned comments into TF-IDF feature vectors."""
    df = pd.read_csv(DATA_PROCESSED)
    sentence_transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
    features = sentence_transformer_model.encode(df["comment"], convert_to_tensor=True)
    feature_data = pd.DataFrame(features.cpu().numpy())
    feature_data["label"] = df["label"]
    # Save vectorized features
    feature_data.to_csv(os.path.join(FEATURES_DIR, "features.csv"), index=False)
    torch.save(features, os.path.join(FEATURES_DIR, "sentence_embeddings.pt"))
    print(f"Sentence embeddings saved to {FEATURES_DIR}/features.csv")

if __name__ == "__main__":
    extract_features()

