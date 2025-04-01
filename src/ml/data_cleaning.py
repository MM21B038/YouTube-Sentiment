import re
import string
import emoji
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import pandas as pd
import os
nltk.download("stopwords")

DATA_RAW = "data/raw/comments.csv"
DATA_PROCESSED = "data/processed"
os.makedirs(DATA_PROCESSED, exist_ok=True)

class clean_comments:
    def __init__(self):
        self.stemmer = SnowballStemmer("english")
        self.stopwords = stopwords.words('english')
    
    def replace_links_with_text(self, text):
        return re.sub(r'https?://\S+|www\.\S+', 'link', text)

    def convert_emoji_to_text(self, text):
        return emoji.demojize(text, language='en').replace(":", " ").replace("_", " ").replace("  ", " ") 
    
    def remove_punctuation(self, text):
        return "".join([c for c in text if c not in string.punctuation])

    def stopwords_stemming_punctuation(self, text):
        words = text.split()
        processed_words = [
            self.stemmer.stem(word.lower())
            for word in words
            if word.lower() not in self.stopwords
        ]
        joined_text = ' '.join(processed_words)
        final_text = self.remove_punctuation(joined_text)
        return final_text

    def transform(self, DATA_RAW):
        df = pd.read_csv(DATA_RAW)
        df = df.dropna(subset=["comment"])  # Remove NaN comments
        df = df[df["comment"].apply(lambda x: isinstance(x, str))]
        df["comment"] = df["comment"].apply(self.replace_links_with_text)
        df["comment"] = df["comment"].apply(self.convert_emoji_to_text)
        df["comment"] = df["comment"].apply(self.stopwords_stemming_punctuation)
        df.to_csv(os.path.join(DATA_PROCESSED, "cleaned_comments.csv"), index=False)
        print(f"Cleaned comments saved to {DATA_PROCESSED}/cleaned_comments.csv")

if __name__ == "__main__":
    cleaner = clean_comments()
    cleaner.transform(DATA_RAW)