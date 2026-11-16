# Classifier evaluation notes

The reproducible training script creates a grouped 75/25 train/test split from 336 synthetic utterances (252 train, 84 test). A local reproduction of the current training code produced 36.9% held-out accuracy. This is weak performance and should be discussed honestly in the portfolio; the model needs more varied, representative training examples and error analysis before practical use.

The app currently uses a confidence threshold of 0.30 as a conservative demonstration setting, not as a validated production threshold. On the reproduced test split, approximately 58.3% of examples exceeded that threshold, and accuracy among those accepted predictions was approximately 44.9%. The threshold is therefore provisional. Low-confidence messages use a fallback rather than being treated as known intents.

The dataset is synthetic and small. It does not represent real EventArena users, and synthetic held-out results do not establish real-world accuracy. Record actual routes and confidence values during your live demonstrations, and update this report if you change the dataset, model, or threshold.

## Class-wise results from the reproduced split

| Intent | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| cheap | 0.67 | 0.50 | 0.57 | 16 |
| concerts | 0.22 | 0.33 | 0.27 | 12 |
| festivals | 0.15 | 0.25 | 0.19 | 8 |
| goodbye | 0.53 | 0.75 | 0.62 | 12 |
| greeting | 1.00 | 0.25 | 0.40 | 16 |
| help | 1.00 | 0.50 | 0.67 | 8 |
| sports | 0.00 | 0.00 | 0.00 | 12 |

Overall accuracy: 0.37 (84 held-out examples).