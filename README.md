# YouTube Comment Sentiment Analysis

## Overview
This project performs sentiment analysis on YouTube comments using natural language processing (NLP) and machine learning techniques. The pipeline includes data cleaning, feature engineering, model training, and deployment using **DVC (Data Version Control)** and **GitHub Actions for CI/CD**.

## Features
- Data collection and preprocessing of YouTube comments
- Feature extraction using **Sentence Transformers**
- Model training using **XGBoost**
- Experiment tracking with **MLflow**
- CI/CD pipeline for automated model training and deployment
- Deployment using **FastAPI** for serving predictions

## Project Structure
```
.
├── data
│   ├── raw                # Raw data (YouTube comments CSV)
│   ├── processed          # Cleaned data and extracted features
│
├── models                 # Trained machine learning models
│   ├── xg_model.pkl       # XGBoost trained model
│   ├── label_encoder.pkl  # Label encoder for sentiment labels
│
├── src
│   ├── ml
│   │   ├── data_cleaning.py        # Data preprocessing
│   │   ├── feature_engineering.py  # Feature extraction
│   │   ├── train.py                # Model training
│   │   ├── promote_model.py        # Model promotion
│   │   ├── inference.py            # Model inference for API
│
├── api
│   ├── app.py              # FastAPI application for serving predictions
│
├── mlruns                 # MLflow tracking
├── dvc.yaml               # DVC pipeline configuration
├── requirements.txt       # Python dependencies
├── ci.yml                 # GitHub Actions CI/CD pipeline
├── Dockerfile             # Containerization setup
└── README.md              # Project documentation
```

## Installation
To set up the project locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/YouTube-Sentiment-Analysis.git
   cd YouTube-Sentiment-Analysis
   ```

2. Create a virtual environment and install dependencies:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Install and initialize **DVC**:
   ```sh
   pip install dvc[all]
   dvc init
   dvc pull  # Fetch the latest dataset and models
   ```

## Running the Pipeline
To execute the full pipeline:
```sh
dvc repro
```
This will:
- Clean the raw data
- Extract features using sentence transformers
- Train an XGBoost model
- Save the trained model and classification report

## Running the API
To start the FastAPI server for serving predictions:
```sh
uvicorn api.app:app --host 0.0.0.0 --port 8000
```

## CI/CD Workflow
- The **GitHub Actions CI/CD pipeline** is triggered on every `push` or `pull request` to the `main` branch.
- It installs dependencies, pulls DVC data, runs the pipeline, and promotes the trained model.
- The latest model is deployed using **FastAPI** in a Docker container.

## Contributing
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes.
4. Push the branch and submit a pull request.

## License
This project is licensed under the MIT License.


