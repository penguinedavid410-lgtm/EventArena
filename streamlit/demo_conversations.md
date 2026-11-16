# Live demonstration scripts

These are test scripts, not screenshots or proof of a live run. Run the app and record the actual route and confidence displayed for each input. Capture genuine screenshots of two separate conversations for your assessment.

## Conversation 1 — event discovery

1. `Hello` — expected greeting rule.
2. `who is performing this month?` — intended classifier test (does not contain the rule keywords for concerts).
3. `I'd love to visit a local fair` — intended classifier test (the rule list does not include “fair”).
4. `I need something affordable` — intended classifier test (the rule list does not include “affordable”).
5. `tell me about upcoming competitions` — intended classifier test; check actual predicted class and confidence.

## Conversation 2 — help and fallback

1. `What can you do?` — help rule.
2. `Can you book me a flight to the moon?` — intended out-of-domain test; check whether the model confidence is below threshold. If not, note the limitation and test another unrelated phrase.
3. `show upcoming rugby fixtures` — sports rule.
4. `goodbye` — goodbye rule.

At least three paraphrases must be visibly handled by the classifier rather than the rules. Keep the app's route/confidence captions visible in screenshots.
