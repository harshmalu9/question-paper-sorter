from rag.llm_engine import LLMEngine


class QAEngine:

    def __init__(self):

        self.llm = LLMEngine()

    def answer(
        self,
        query: str,
        context: str,
    ) -> str:

        return self.llm.generate_answer(
            query, context
        )
