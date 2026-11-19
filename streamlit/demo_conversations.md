# EventArena — test conversations

These are test prompts, not screenshots or evidence of a live run. Launch the Streamlit app and capture your own screenshots.

## Opening screen

Expected wording:

> Hello! Welcome to EventArena.
>
> Do you want to ask about one of these suggestions?
>
> 1. What sports events are coming up?
> 2. Which concerts can I attend?
> 3. What festivals are happening?
> 4. What free or low-cost events are available?
> 5. How do I find an event's date, venue and ticket price?

The screen also has a separate **Help** button and a text input.

## Conversation 1 — event suggestions

1. Click **Sports events** — expect sports sample listings.
2. Click **Concerts** — expect concert sample listings.
3. Click **Festivals** — expect festival sample listings.
4. Click **Cheap or free events** — expect free and low-cost sample listings.
5. Click **Event information**, then type **When is Acoustic Live Sessions?** — expect its sample date, venue and ticket price.

## Conversation 2 — paraphrases, help and fallback

1. Type **Hello** — expect the greeting.
2. Type **who is performing this month?** — inspect whether the classifier handles this paraphrase.
3. Type **I'd love to visit a local fair** — inspect whether the classifier handles this paraphrase.
4. Type **activities that won't break the bank** — inspect whether the classifier handles this paraphrase.
5. Click **Help** — expect an explanation of supported topics.
6. Type **Can you diagnose my car and calculate my tax?** — check whether low confidence triggers fallback; record the actual result.
7. Type **Goodbye** — expect the closing response.

## Evidence checklist

- [ ] Capture the welcome message and five suggested questions.
- [ ] Capture the separate Help response.
- [ ] Capture two distinct conversations.
- [ ] Show at least three messages actually handled by classifier rather than rules.
- [ ] Show an actual fallback response.
- [ ] Do not describe fictional sample listings as verified live events.
