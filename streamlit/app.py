from pathlib import Path
import re
import joblib
import streamlit as st
from train_model import MODEL, THRESHOLD, train_and_save

if not MODEL.exists():
    train_and_save()
classifier = joblib.load(MODEL)

EVENTS = [
    {"name":"Kigali City Football Final","category":"sports","date":"2026-11-21","venue":"Amahoro Stadium","price":5},
    {"name":"East Africa Basketball Night","category":"sports","date":"2026-11-24","venue":"BK Arena","price":8},
    {"name":"Acoustic Live Sessions","category":"concerts","date":"2026-11-22","venue":"Kigali Cultural Village","price":12},
    {"name":"Jazz Under the Stars","category":"concerts","date":"2026-11-28","venue":"Kigali Convention Centre","price":15},
    {"name":"Kigali Food and Culture Fair","category":"festivals","date":"2026-11-23","venue":"Imbuga City Walk","price":3},
    {"name":"Creative Arts Weekend","category":"festivals","date":"2026-11-29","venue":"Kigali Public Library","price":4},
    {"name":"Community Movie Evening","category":"cheap","date":"2026-11-20","venue":"Kimironko Community Hall","price":0},
    {"name":"Open-Air Fitness Meetup","category":"cheap","date":"2026-11-26","venue":"Kigali Sports Park","price":1}
]

def rule_intent(message):
    text = message.lower().strip()
    rules = [
        ("greeting", r"^(hi|hello|hey|good morning|good afternoon|good evening)\b"),
        ("goodbye", r"\b(bye|goodbye|exit|quit|farewell)\b"),
        ("help", r"\b(help|what can you do|how do i use)\b"),
        ("sports", r"\b(sport|football|basketball|tennis|rugby)\b"),
        ("concerts", r"\b(concert|music|gig|band)\b"),
        ("festivals", r"\b(festival|carnival|celebration)\b"),
        ("cheap", r"\b(cheap|free|budget|low cost)\b")
    ]
    for intent, pattern in rules:
        if re.search(pattern, text):
            return intent
    return None

def answer_for(intent):
    if intent == "greeting":
        return "Hello! Welcome to EventArena. Ask me about sports, concerts, festivals, or affordable events."
    if intent == "help":
        return "I can help you discover sports events, concerts, festivals, and low-cost activities. Describe what you would enjoy."
    if intent == "goodbye":
        return "Thanks for visiting EventArena. See you next time!"
    matches = [item for item in EVENTS if item["category"] == intent or (intent == "cheap" and item["price"] <= 5)]
    if not matches:
        return "I couldn't find a matching event in the sample event list."
    return "Here are some matching events:\n\n" + "\n".join(
        f"- **{item['name']}** — {item['date']} at {item['venue']} | {item['price']} USD" for item in matches
    )

def respond(message):
    rule = rule_intent(message)
    if rule:
        return answer_for(rule), f"rule:{rule}", 1.0
    probabilities = classifier.predict_proba([message])[0]
    index = probabilities.argmax()
    intent, confidence = classifier.classes_[index], float(probabilities[index])
    if confidence < THRESHOLD:
        return ("I'm not confident I understood. Try sports, concerts, festivals, affordable events, or type 'help'.",
                "fallback:low_confidence", confidence)
    return answer_for(intent), f"classifier:{intent}", confidence

st.set_page_config(page_title="EventArena Chatbot", page_icon="🎟️")
st.title("🎟️ EventArena")
st.caption("Discover sports, concerts, festivals, and affordable things to do.")
with st.sidebar:
    st.subheader("About")
    st.write("Hybrid intent detection: keyword rules first, then TF-IDF + Logistic Regression.")
    st.write(f"Confidence threshold: **{THRESHOLD:.2f}**")
    st.write("Try paraphrases such as 'who is performing this month?' or 'I need something affordable'.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"Hello! I'm EventArena. What kind of event are you looking for?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about events...")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    reply, route, confidence = respond(prompt)
    st.session_state.messages.append({"role":"assistant","content":reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
        st.caption(f"Handled by {route} · confidence {confidence:.2f}")
