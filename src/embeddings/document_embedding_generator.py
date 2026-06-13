class DocumentEmbeddingGenerator:

    def __init__(
        self,
        model
    ):
        self.model = model

    def generate(
        self,
        text: str
    ):
        return self.model.encode(
            text
        )
