import json
import urllib.request
import urllib.error

from pathlib import Path


CONFIG_PATH = "config/model_config.json"
OLLAMA_API = (
    "http://localhost:11434/api/generate"
)
DEFAULT_MODEL = "phi3"


def _load_model_name() -> str:

    path = Path(CONFIG_PATH)

    if not path.exists():
        return DEFAULT_MODEL

    try:

        with open(path) as f:
            config = json.load(f)

        return config.get(
            "ollama_model", DEFAULT_MODEL
        )

    except (
        json.JSONDecodeError,
        OSError,
    ):
        return DEFAULT_MODEL


PROMPT_TEMPLATE = """You are a document question-answering assistant.

Use ONLY the provided context.

Answer ONLY information directly relevant to the user question.
Ignore unrelated sections even if present in context.

If answer is not present, reply:
"Answer not found in documents."

Be concise and accurate.

Question:
{query}

Context:
{context}

Answer:"""


class LLMEngine:

    def __init__(
        self,
        model: str = None,
        api_url: str = OLLAMA_API,
    ):

        if model is None:
            model = _load_model_name()

        self.model = model
        self.api_url = api_url

    def _build_prompt(
        self,
        query: str,
        context: str,
    ) -> str:

        return PROMPT_TEMPLATE.format(
            query=query, context=context
        )

    def generate_answer(
        self,
        query: str,
        context: str,
    ) -> str:

        prompt = self._build_prompt(
            query, context
        )

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        data = json.dumps(
            payload
        ).encode("utf-8")

        req = urllib.request.Request(
            self.api_url,
            data=data,
            headers={
                "Content-Type":
                    "application/json"
            },
        )

        try:

            with urllib.request.urlopen(
                req, timeout=120
            ) as resp:

                result = json.loads(
                    resp.read()
                )

                return result.get(
                    "response", ""
                ).strip()

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            ConnectionRefusedError,
            OSError,
        ):

            return (
                "LLM unavailable. "
                "Falling back to "
                "keyword mode."
            )
