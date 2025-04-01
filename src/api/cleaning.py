import re
import string
import emoji
import joblib
import nltk
nltk.download('stopwords')
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer

sentence_transformer_model = SentenceTransformer('all-MiniLM-L6-v2')


class CustomTextToVector:
    def __init__(self):
        self.stemmer = SnowballStemmer("english")
        self.stopwords = stopwords.words('english')
    
    def replace_links_with_text(self, text):
        return re.sub(r'https?://\S+|www\.\S+', 'link', text)

    def convert_emoji_to_text(self, text):
        return emoji.demojize(text, language='en').replace(":", " ").replace("_", " ").replace("  ", " ") 
    
    def remove_punctuation(self, text):
        return "".join([c for c in text if c not in string.punctuation])

    def st_pca(self, text):
        sentence_embeddings = sentence_transformer_model.encode([text])
        return sentence_embeddings

    def transform(self, comments):
        processed_texts = []
        for comment in comments:
            processed_text = self.replace_links_with_text(comment)
            processed_text = self.convert_emoji_to_text(processed_text)
            words = processed_text.split()
            processed_words = [
                self.stemmer.stem(word.lower())
                for word in words
                if word.lower() not in self.stopwords
            ]
            joined_text = ' '.join(processed_words)
            final_text = self.remove_punctuation(joined_text)
            processed_texts.append(final_text)

        return [self.st_pca(text) for text in processed_texts]