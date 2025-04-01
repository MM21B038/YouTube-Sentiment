import pandas as pd
import os

source_path = "data/raw/data.pkl"
DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

def load_dataset(source_path):
    """Loads labeled dataset from data.pkl and saves as CSV."""
    df = pd.read_pickle(source_path)
    df.columns = ['comment', 'label']
    df.to_csv(os.path.join(DATA_DIR, "comments.csv"), index=False)
    print(f"Dataset loaded and saved to {DATA_DIR}/comments.csv")
    
if __name__ == "__main__":
    load_dataset(source_path)