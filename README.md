# EventArena — Portfolio Project 2, Part 2

A Streamlit event-discovery chatbot demonstrating hybrid rule-based and machine-learning intent detection. It uses a TF-IDF + Logistic Regression classifier trained from a reproducible synthetic dataset, with a confidence threshold and an out-of-scope fallback.

## Run locally

```bash
cd streamlit
python -m venv .venv
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

The training script creates intents.csv, intent_classifier.joblib, and evaluation_report.md. The app also trains the model automatically on first launch if the model file is missing.

## Structure
- streamlit/app.py — chatbot UI, rules, classifier integration, confidence fallback, and sample event responses.
- streamlit/train_model.py — synthetic data generation, grouped train/test split, training, and evaluation.
- streamlit/demo_conversations.md — two conversation scripts and classifier-only paraphrase tests.
- streamlit/requirements.txt — dependencies.

## Streamlit deployment
Push this repository to GitHub, create an app in Streamlit Community Cloud, select this repository, set the main file path to streamlit/app.py, and deploy. No API key or bot token is required.

## Notes
The synthetic dataset is educational test material, not real user data. Review evaluation_report.md after training and discuss limitations of synthetic data. Run the app and capture genuine screenshots of at least two separate conversations for your portfolio; the supplied demo scripts are not screenshots or proof of a live run. Never commit passwords, access tokens, or private user data.
