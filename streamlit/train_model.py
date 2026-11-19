from pathlib import Path
import pandas as pd
import joblib
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

BASE = Path(__file__).resolve().parent
MODEL, DATA, REPORT = BASE / "intent_classifier.joblib", BASE / "intents.csv", BASE / "evaluation_report.md"
THRESHOLD = 0.35  # provisional demo setting, not calibrated on real conversations

PHRASES = {
"sports": ["show me sports events","what games are coming up","find sporting events","any football matches soon","I want to attend a basketball game","when is the next marathon","show upcoming rugby fixtures","are there tennis tournaments","where can I watch a live game","tell me about upcoming competitions","I fancy watching a match","what teams are playing soon","any athletics meets this month","show me upcoming matches","is there a tournament soon"],
"concerts": ["show me concerts","what live music is happening","find music gigs","any bands playing soon","who is performing this month","show upcoming music shows","are there jazz performances","where can I hear live music","tell me about upcoming gigs","I fancy a night of music","what artists are performing","I want tickets for a music show","any singers coming to town","where can I listen to a band","list live performances"],
"festivals": ["show me festivals","what cultural festivals are coming up","find community celebrations","any food festivals soon","I'd love to visit a local fair","what celebrations are scheduled","show upcoming cultural events","are there film festivals","tell me about upcoming fairs","I fancy a festival","when is the next community fair","what festivals are on this weekend","any arts celebrations","where is the next cultural gathering","show me local fairs"],
"cheap": ["show me cheap events","find affordable things to do","events under ten dollars","I am on a tight budget","what free events are available","find low cost activities","anything inexpensive this weekend","show budget friendly events","I need something affordable","what are the cheapest events","I want inexpensive tickets","can I do something fun for free","activities that won't break the bank","show no cost activities","find events for less than five dollars"],
"event_details": ["when is Acoustic Live Sessions","where is Jazz Under the Stars","how much is the ticket for Kigali City Football Final","tell me the venue for East Africa Basketball Night","what date is the Kigali Food and Culture Fair","give me information about Community Movie Evening","I need the price for Creative Arts Weekend","where does Open-Air Fitness Meetup take place","what is the event date","tell me more about a listed event","I want the location and cost of an event","give me event details","how much does entry cost","where will it happen","can you provide the venue"],
"greeting": ["hello","hi there","good morning","hey EventArena","howdy","is anyone there","good evening","hiya","hello assistant","can we chat","greetings","good afternoon"],
"help": ["help","what can you do","show me how this works","I need assistance","what options do I have","explain the options","how do I use EventArena","what features are available","tell me how to search","give me instructions","how does this chatbot work","can you assist me"],
"goodbye": ["bye","goodbye","see you later","that's all thanks","exit","quit","talk to you soon","farewell","I'm done","catch you later","end this conversation","take care"]
}

def build_dataset():
    rows = []
    for intent, phrases in PHRASES.items():
        for i, phrase in enumerate(phrases):
            for text in (phrase, "please " + phrase, "could you " + phrase + "?", phrase + " please"):
                rows.append({"text":text,"intent":intent,"group":f"{intent}_{i}"})
    return pd.DataFrame(rows)

def train_and_save():
    df = build_dataset()
    split = GroupShuffleSplit(n_splits=1,test_size=0.25,random_state=42)
    train_idx,test_idx = next(split.split(df.text,df.intent,groups=df.group))
    train,test = df.iloc[train_idx],df.iloc[test_idx]
    model = Pipeline([
        ("tfidf",TfidfVectorizer(ngram_range=(1,2),strip_accents="unicode",sublinear_tf=True)),
        ("classifier",LogisticRegression(max_iter=2000,class_weight="balanced",C=2.0))
    ])
    model.fit(train.text,train.intent)
    predicted = model.predict(test.text)
    score = accuracy_score(test.intent,predicted)
    joblib.dump(model,MODEL)
    df.drop(columns="group").to_csv(DATA,index=False)
    REPORT.write_text(
        "# EventArena classifier evaluation\n\n"
        f"- Synthetic utterances: {len(df)}\n- Training utterances: {len(train)}\n"
        f"- Held-out utterances: {len(test)}\n- Held-out accuracy: {score:.3f}\n"
        f"- Provisional confidence threshold: {THRESHOLD:.2f}\n\n"
        "Variants of each authored phrase remain in one split group. This is a small synthetic dataset; "
        "the threshold is not calibrated on real user conversations and the score does not prove real-world accuracy.\n\n"
        "## Classification report\n\n" + classification_report(test.intent,predicted,zero_division=0),
        encoding="utf-8")
    return model,score

if __name__ == "__main__":
    _,score = train_and_save()
    print(f"Model saved to {MODEL}; held-out accuracy={score:.3f}")
