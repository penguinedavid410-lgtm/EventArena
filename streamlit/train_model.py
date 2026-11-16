from pathlib import Path
import pandas as pd
import joblib
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

HERE = Path(__file__).resolve().parent
MODEL = HERE / "intent_classifier.joblib"
DATA = HERE / "intents.csv"
REPORT = HERE / "evaluation_report.md"
THRESHOLD = 0.30

PHRASES = {
"sports": ["show me sports events", "what games are coming up", "find sporting events", "any football matches soon", "I want to attend a basketball game", "when is the next marathon", "show upcoming rugby fixtures", "are there any tennis tournaments", "where can I see a live game", "tell me about upcoming competitions", "I fancy watching some sport", "what teams are playing soon"],
"concerts": ["show me concerts", "what live music is happening", "find music gigs", "any bands playing soon", "who is performing this month", "show upcoming music shows", "are there jazz performances", "where can I hear live music", "tell me about upcoming gigs", "I fancy a night of music", "what artists are performing", "I want tickets for a music show"],
"festivals": ["show me festivals", "what cultural festivals are coming up", "find community celebrations", "any food festivals soon", "I'd love to visit a local fair", "what celebrations are scheduled", "show upcoming cultural events", "are there film festivals", "tell me about upcoming fairs", "I fancy a festival", "when is the next community fair", "what festivals are on this weekend"],
"cheap": ["show me cheap events", "find affordable things to do", "events under ten dollars", "I am on a tight budget", "what free events are available", "find low cost activities", "anything inexpensive this weekend", "show budget friendly events", "I need something affordable", "what are the cheapest events", "I want inexpensive tickets", "can I do something fun for free"],
"greeting": ["hello", "hi there", "good morning", "hey EventArena", "howdy", "is anyone there", "good evening", "hiya", "hello assistant", "can we chat", "greetings", "what's up"],
"help": ["help", "what can you do", "show me how this works", "I need assistance", "what options do I have", "explain the commands", "how do I use EventArena", "what features are available", "tell me how to search", "give me instructions", "how does this chatbot work", "can you assist me"],
"goodbye": ["bye", "goodbye", "see you later", "that's all thanks", "exit", "quit", "talk to you soon", "farewell", "I'm done", "catch you later", "end this conversation", "take care"]
}

def train_and_save():
    rows = []
    for intent, phrases in PHRASES.items():
        for i, phrase in enumerate(phrases):
            for text in [phrase, "please " + phrase, "could you " + phrase, phrase + " please"]:
                rows.append({"text": text, "intent": intent, "group": f"{intent}_{i}"})
    df = pd.DataFrame(rows)
    split = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
    train_i, test_i = next(split.split(df.text, df.intent, groups=df.group))
    train, test = df.iloc[train_i], df.iloc[test_i]
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), strip_accents="unicode", sublinear_tf=True)),
        ("classifier", LogisticRegression(max_iter=1500, class_weight="balanced", C=3))
    ])
    model.fit(train.text, train.intent)
    predictions = model.predict(test.text)
    score = accuracy_score(test.intent, predictions)
    report = classification_report(test.intent, predictions, zero_division=0)
    joblib.dump(model, MODEL)
    df.drop(columns="group").to_csv(DATA, index=False)
    REPORT.write_text(
        "# EventArena classifier evaluation\n\n"
        f"- Synthetic examples: {len(df)}\n- Training examples: {len(train)}\n"
        f"- Held-out examples: {len(test)}\n- Held-out accuracy: {score:.3f}\n"
        f"- App confidence threshold: {THRESHOLD:.2f}\n\n"
        "Paraphrase variants are grouped with their source utterance before splitting. "
        "This small synthetic test is not evidence of real-world performance.\n\n"
        "Classification report:\n\n" + report,
        encoding="utf-8"
    )
    return model, score

if __name__ == "__main__":
    _, score = train_and_save()
    print(f"Model saved to {MODEL}; held-out accuracy={score:.3f}")
