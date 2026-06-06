from classification.embedding_classifier import (
    EmbeddingClassifier
)

cache_file = "data/cache/ocr/page_009.txt"

with open(
    cache_file,
    "r",
    encoding="utf-8"
) as file:

    text = file.read()

classifier = EmbeddingClassifier()

subject, scores = classifier.classify(
    text
)

print("\nPredicted Subject:")
print(subject)

print("\nScores:")

for subject, score in sorted(
    scores.items(),
    key=lambda x: x[1],
    reverse=True
):
    print(
        f"{subject}: {score:.4f}"
    )