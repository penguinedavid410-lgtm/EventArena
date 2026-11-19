# Classifier evaluation and limitations

Run `python train_model.py` to regenerate `evaluation_report.md` from the current dataset and model. Report the score from that run in your portfolio.

The classifier uses TF-IDF and Logistic Regression for eight intents: sports, concerts, festivals, cheap, event_details, greeting, help, and goodbye. Obvious keyword phrases are handled by rules first; unmatched paraphrases go to the classifier. Predictions below the confidence threshold use a fallback.

The threshold in `train_model.py` is 0.35. It is provisional and not calibrated on real user conversations. Confidence is not the same as measured accuracy.

The dataset is synthetic and authored for coursework. Grouped splitting keeps generated variants of each phrase together, reducing near-duplicate leakage, but the dataset is small and does not represent real users. Test with new phrases, record actual routes and confidence values, and discuss errors.

All event listings in `app.py` are fictional sample records, not live or verified events.
