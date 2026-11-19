from pathlib import Path
import re
import joblib
import streamlit as st
from train_model import MODEL, THRESHOLD, train_and_save

st.set_page_config(page_title="EventArena", page_icon="🎟️", layout="centered")
if not MODEL.exists():
    train_and_save()
classifier = joblib.load(MODEL)

# Fictional sample records for coursework demonstration only.
EVENTS = [
    {"name":"Kigali City Football Final","category":"sports","date":"22 Nov 2026","venue":"Amahoro Stadium","price":5},
    {"name":"East Africa Basketball Night","category":"sports","date":"24 Nov 2026","venue":"BK Arena","price":8},
    {"name":"Acoustic Live Sessions","category":"concerts","date":"22 Nov 2026","venue":"Kigali Cultural Village","price":12},
    {"name":"Jazz Under the Stars","category":"concerts","date":"28 Nov 2026","venue":"Kigali Convention Centre","price":15},
    {"name":"Kigali Food and Culture Fair","category":"festivals","date":"23 Nov 2026","venue":"Imbuga City Walk","price":3},
    {"name":"Creative Arts Weekend","category":"festivals","date":"29 Nov 2026","venue":"Kigali Public Library","price":4},
    {"name":"Community Movie Evening","category":"cheap","date":"21 Nov 2026","venue":"Kimironko Community Hall","price":0},
    {"name":"Open-Air Fitness Meetup","category":"cheap","date":"26 Nov 2026","venue":"Kigali Sports Park","price":1},
]
OPTIONS = [
    ("🏟️ Sports events", "Show me upcoming sports events."),
    ("🎵 Concerts", "Show me upcoming concerts."),
    ("🎉 Festivals", "Show me upcoming festivals."),
    ("💸 Cheap or free events", "Show me affordable and free events."),
    ("ℹ️ Event information", "How can I get an event date, venue, or ticket price?"),
    ("❓ Help", "What can you help me with?"),
]

def detect_rule(text):
    rules = [
        ("greeting", r"^(hi|hello|hey|good morning|good afternoon|good evening)\b"),
        ("goodbye", r"\b(bye|goodbye|exit|quit|farewell)\b"),
        ("help", r"\b(help|what can you do|how do i use)\b"),
        ("sports", r"\b(sports? events?|football|basketball|tennis|rugby)\b"),
        ("concerts", r"\b(concerts?|music events?|gigs?)\b"),
        ("festivals", r"\b(festivals?|carnivals?)\b"),
        ("cheap", r"\b(cheap|free|budget|low[- ]cost)\b"),
    ]
    for intent, pattern in rules:
        if re.search(pattern, text.lower().strip()):
            return intent
    return None

def answer(intent, message):
    if intent == "greeting":
        return "Hello! Welcome to EventArena. How can I help you today? Please choose one of the options below."
    if intent == "help":
        return "I can help with sports events, concerts, festivals, cheap or free events, and event date, venue, and ticket price. Choose an option or type a question."
    if intent == "goodbye":
        return "Thanks for visiting EventArena. Have a great day!"
    if intent == "event_details":
        text = message.lower()
        for item in EVENTS:
            if item["name"].lower() in text:
                return (f"**{item['name']}**\n\n- Date: {item['date']}\n- Venue: {item['venue']}\n"
                        f"- Ticket price: {item['price']} USD")
        return "Please include the event name. Example: **When is Acoustic Live Sessions?**"
    matches = [item for item in EVENTS if item["category"] == intent or (intent == "cheap" and item["price"] <= 5)]
    if not matches:
        return "I don't have a matching sample listing. Please choose one of the categories shown above."
    heading = {"sports":"🏟️ Upcoming sports events","concerts":"🎵 Upcoming concerts",
               "festivals":"🎉 Upcoming festivals","cheap":"💸 Cheap or free events"}[intent]
    rows = [f"- **{x['name']}** — {x['date']} · {x['venue']} · {x['price']} USD" for x in matches]
    return heading + "\n\n" + "\n".join(rows) + "\n\n*Fictional sample listings for coursework; not verified live events.*"

def respond(message):
    rule = detect_rule(message)
    if rule:
        return answer(rule, message), f"rule:{rule}", 1.0
    probabilities = classifier.predict_proba([message])[0]
    idx = probabilities.argmax()
    intent, confidence = classifier.classes_[idx], float(probabilities[idx])
    if confidence < THRESHOLD:
        return ("Sorry, I didn't understand that. I can help with sports, concerts, festivals, cheap or free events, "
                "event information, and help. Please choose an option below.",
                "fallback:low_confidence", confidence)
    return answer(intent, message), f"classifier:{intent}", confidence

st.title("🎟️ EventArena")
st.caption("Your simple guide to discovering events.")
if "messages" not in st.session_state:
    welcome = ("Hello! Welcome to EventArena. How can I help you today?\n\n"
               "Please choose one of the following options:\n\n" +
               "\n".join(f"{i+1}. {label}" for i, (label, _) in enumerate(OPTIONS)))
    st.session_state.messages = [{"role":"assistant","content":welcome}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("route"):
            st.caption(f"Handled by {msg['route']} · confidence {msg['confidence']:.2f}")

def submit(text):
    reply, route, confidence = respond(text)
    st.session_state.messages.append({"role":"user","content":text})
    st.session_state.messages.append({"role":"assistant","content":reply,"route":route,"confidence":confidence})

st.subheader("Choose what you need")
cols = st.columns(2)
for i, (label, question) in enumerate(OPTIONS):
    if cols[i % 2].button(label, key=f"option_{i}", use_container_width=True):
        submit(question)
        st.rerun()
typed = st.chat_input("Or type a question about events...")
if typed:
    submit(typed)
    st.rerun()

with st.sidebar:
    st.subheader("Questions I can answer")
    st.markdown("- Sports events\n- Concerts\n- Festivals\n- Cheap or free events\n- Event date, venue, and ticket price\n- Help and greetings")
    st.caption(f"Classifier confidence threshold: {THRESHOLD:.2f} (provisional)")
    st.caption("Sample listings are fictional, not live listings.")
