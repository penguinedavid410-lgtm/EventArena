# EventArena — Portfolio Project 2, Part 2

EventArena is a focused Streamlit chatbot for discovering sample sports events, concerts, festivals, and affordable activities. It demonstrates hybrid intent recognition: keyword rules for obvious phrases, a TF-IDF + Logistic Regression classifier for paraphrases, and a low-confidence fallback.

## What users see first

> Hello! Welcome to EventArena. How can I help you today?

The chatbot displays six selectable choices: Sports events, Concerts, Festivals, Cheap or free events, Event information (date, venue, ticket price), and Help. Users can also type their own question. The assistant stays within these topics and falls back on unsupported questions.

## Run locally

```bash
cd streamlit
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

The training script creates `intents.csv`, `intent_classifier.joblib`, and `evaluation_report.md`. If the model is missing, the app trains it automatically on first launch.

## Deploy on Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud.
2. Click **New app** and select this GitHub repository.
3. Select branch `main`.
4. Set **Main file path** to `streamlit/app.py`.
5. Deploy. Dependencies are in `streamlit/requirements.txt`.

No API key or bot token is required.

## Assessment evidence

Use `streamlit/demo_conversations.md` for two test scripts. Run the app and capture genuine screenshots of the welcome menu, at least three classifier-handled paraphrases, a fallback, and two separate conversations. The app displays route and confidence below assistant replies.

## Limitations

Event listings are fictional sample records, not live listings. The classifier uses synthetic authored examples; report the score from your own training run. The confidence threshold is provisional and not a production guarantee. Never commit credentials or private information.
