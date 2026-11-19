# EventArena — live test scripts

These are test scripts, not screenshots or evidence of a live run. Launch the app and capture your own screenshots with route/confidence captions visible.

## Opening message

> Hello! Welcome to EventArena. How can I help you today?
>
> Please choose one of the following options:
> 1. Sports events
> 2. Concerts
> 3. Festivals
> 4. Cheap or free events
> 5. Event information
> 6. Help

## Conversation 1 — event discovery and classifier paraphrases

1. `Hello` — expected rule:greeting.
2. `who is performing this month?` — classifier test for concerts.
3. `I'd love to visit a local fair` — classifier test for festivals.
4. `activities that won't break the bank` — classifier test for cheap events.
5. `When is Acoustic Live Sessions?` — classifier test for event_details.

Verify that at least three actually display `classifier:` rather than `rule:`.

## Conversation 2 — menu, help, and fallback

1. Select Sports events — expected sports response.
2. `What can you help me with?` — expected help response.
3. `Can you diagnose my car and calculate my tax?` — intended out-of-scope test; record the actual result. If accepted by the classifier, note the limitation and test another unrelated phrase.
4. `Goodbye` — expected goodbye response.

## Evidence checklist

- [ ] Capture the welcome message and six choices.
- [ ] Capture two separate conversations.
- [ ] Show at least three classifier-handled paraphrases.
- [ ] Show one fallback response.
- [ ] Do not present fictional sample events as verified live listings.
