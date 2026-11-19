from pathlib import Path
import re
import joblib
import streamlit as st
from train_model import MODEL, THRESHOLD, train_and_save

st.set_page_config(page_title="EventArena | Event discovery", page_icon="🎟️", layout="centered")
if not MODEL.exists():
    train_and_save()
classifier = joblib.load(MODEL)

# Fictional sample records for coursework demonstration, not live event listings.
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
SUGGESTIONS = [
    ("Sports events", "What sports events are coming up?"),
    ("Concerts", "Which concerts can I attend?"),
    ("Festivals", "What festivals are happening?"),
    ("Cheap or free events", "What free or low-cost events are available?"),
    ("Event information", "How do I find an event's date, venue and ticket price?"),
]

def detect_rule(text):
    value = text.lower().strip()
    rules = [
        ("greeting", r"^(hi|hello|hey|good morning|good afternoon|good evening)\b"),
        ("goodbye", r"\b(bye|goodbye|exit|quit|farewell)\b"),
        ("help", r"\b(help|what can you do|how do i use)\b"),
        ("event_details", r"\b(date|venue|ticket price|entry fee|how much|where is|when is|details)\b"),
        ("sports", r"\b(sports? events?|football|basketball|tennis|rugby|matches?)\b"),
        ("concerts", r"\b(concerts?|live music|music events?|gigs?|performers?)\b"),
        ("festivals", r"\b(festivals?|carnivals?|cultural fairs?)\b"),
        ("cheap", r"\b(cheap|free|budget|low[- ]cost|affordable|inexpensive)\b"),
    ]
    for intent, pattern in rules:
        if re.search(pattern, value):
            return intent
    return None

def list_events(intent):
    found = [event for event in EVENTS if event["category"] == intent]
    if intent == "cheap":
        found = [event for event in EVENTS if event["price"] <= 5]
    heading = {"sports":"Upcoming sports events","concerts":"Upcoming concerts",
               "festivals":"Upcoming festivals","cheap":"Affordable and free activities"}[intent]
    lines = [f"- **{event['name']}** — {event['date']} | {event['venue']} | {event['price']} USD" for event in found]
    return heading + "\n\n" + "\n".join(lines) + "\n\n*Fictional sample listings for coursework; not verified live events.*"

def event_details(message):
    lowered = message.lower()
    for event in EVENTS:
        if event["name"].lower() in lowered:
            return (f"**{event['name']}**\n\n- **Date:** {event['date']}\n"
                    f"- **Venue:** {event['venue']}\n- **Ticket price:** {event['price']} USD\n\n"
                    "*Fictional sample listing for coursework.*")
    names = "\n".join(f"- {event['name']}" for event in EVENTS)
    return ("I can provide the date, venue and ticket price for a listed sample event. Which event would you like to know about?\n\n"
            + names + "\n\nFor example: **When is Acoustic Live Sessions?**")

def answer(intent, message):
    if intent == "greeting":
        return ("Hello! Welcome to EventArena.\n\nChoose one of the questions below, select **Help**, or type your own question.")
    if intent == "help":
        return ("**How EventArena can help**\n\nChoose one of the five suggested questions to browse sports, concerts, "
                "festivals, affordable activities, or event details. You can type an event name to see its sample date, "
                "venue and ticket price. If a question is outside these topics, I will let you know rather than guess.")
    if intent == "goodbye":
        return "Thank you for using EventArena. Have a great day!"
    if intent == "event_details":
        return event_details(message)
    if intent in ("sports", "concerts", "festivals", "cheap"):
        return list_events(intent)
    return "I can help with sports, concerts, festivals, affordable events and event details. Please choose a suggestion or select Help."

def respond(message):
    rule = detect_rule(message)
    if rule:
        return answer(rule, message), f"rule:{rule}", 1.0
    probabilities = classifier.predict_proba([message])[0]
    index = probabilities.argmax()
    intent = classifier.classes_[index]
    confidence = float(probabilities[index])
    if confidence < THRESHOLD:
        return ("I'm sorry, that question is outside the areas I can help with. Please ask about sports, concerts, "
                "festivals, affordable events or event details, or select **Help**.",
                "fallback:low_confidence", confidence)
    return answer(intent, message), f"classifier:{intent}", confidence

st.title("🎟️ EventArena")
st.caption("Discover sports, live music, festivals and affordable activities.")
if "messages" not in st.session_state:
    opening = "Hello! Welcome to EventArena.\n\nChoose one of the questions below, select **Help**, or type your own question."
    st.session_state.messages = [{"role":"assistant","content":opening}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("route"):
            st.caption(f"Handled by {message['route']} | confidence {message['confidence']:.2f}")

def submit_message(text):
    response, route, confidence = respond(text)
    st.session_state.messages.append({"role":"user","content":text})
    st.session_state.messages.append({"role":"assistant","content":response,"route":route,"confidence":confidence})

st.subheader("Suggested questions")
st.caption("Choose a question to see the matching event information.")
columns = st.columns(2)
for index, (label, question) in enumerate(SUGGESTIONS):
    if columns[index % 2].button(label, key=f"suggestion_{index}", use_container_width=True):
        submit_message(question)
        st.rerun()

help_col, _ = st.columns(2)
if help_col.button("Help", key="help_button", use_container_width=True):
    submit_message("Help")
    st.rerun()

typed_question = st.chat_input("Or type your own question about events...")
if typed_question:
    submit_message(typed_question)
    st.rerun()

with st.sidebar:
    st.subheader("Available topics")
    st.markdown("- Sports events\n- Concerts\n- Festivals\n- Cheap or free events\n- Event date, venue and ticket price")
    st.caption(f"Intent classifier threshold: {THRESHOLD:.2f} (provisional)")
    st.caption("Event listings are fictional coursework examples, not live listings.")
