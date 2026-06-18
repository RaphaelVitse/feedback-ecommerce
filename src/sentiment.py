from transformers import pipeline

analyzer = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

def analyze_sentiment(text: str) -> str:
    result = analyzer(text[:512])[0]
    score = int(result["label"].split()[0])

    if score >= 4:
        return "positif"
    elif score == 3:
        return "neutre"
    else:
        return "négatif"
