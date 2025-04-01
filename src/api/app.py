from flask import Flask, request, jsonify
from sentiment_service import predict_sentiment
from comment_extractor import extract_comments
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return "Welcome to the Sentiment Analysis API!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    video_url = data.get('video_url')
    
    if not video_url:
        return jsonify({"error": "No YouTube URL provided"}), 400

    # Extract comments from YouTube video URL
    comments = extract_comments(video_url, 50)
    
    # Get sentiment predictions for all comments
    sentiment_predictions = predict_sentiment(comments)
    
    sentiment_mapping = {1: 'Positive', 0: 'Neutral', -1: 'Negative'}

    # Structure response correctly
    predictions = [
        {"comment": comment, "sentiment": sentiment_mapping[sentiment]}
        for comment, sentiment in zip(comments, sentiment_predictions)
    ]

    # Count the number of sentiments
    sentiment_counts = {
        "Positive": sum(1 for s in sentiment_predictions if s == 1),
        "Neutral": sum(1 for s in sentiment_predictions if s == 0),
        "Negative": sum(1 for s in sentiment_predictions if s == -1),
    }

    return jsonify({"predictions": predictions, "total_comments": len(comments), "sentiment_counts": sentiment_counts})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3333)