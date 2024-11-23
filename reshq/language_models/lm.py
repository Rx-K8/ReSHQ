from typing import Optional

from transformers import pipeline

from reshq.language_models.base import BaseLanguageModel
from reshq.output_parsers.base import BaseOutputParser


class LanguageModel(BaseLanguageModel):
    def __init__(
        self,
        model_id: str,
        output_parser: Optional[BaseOutputParser] = None,
        instruct: Optional[str] = None,
    ):
        self.generator = pipeline("text-generation", model=model_id)
        self.output_parser = output_parser
        self.instruct: Optional[dict[str, str]] = (
            {"role": "assistant", "content": instruct} if instruct else None
        )

    def generate(self, texts: list[str] | str) -> list[str]:
        texts = self._ensure_list(texts)

        prompts = self._create_prompts(texts)
        outputs_with_context = self.generator(prompts)
        outputs = list(
            map(self._parse_last_assistant_output, outputs_with_context)
        )
        if self.output_parser:
            outputs = self._parse_outputs(outputs)

        return outputs

    def _create_prompts(self, texts: list[str]) -> list[list[dict[str, str]]]:
        return list(map(self._to_message, texts))

    def _ensure_list(self, texts: list[str] | str) -> list[str]:
        return [texts] if isinstance(texts, str) else texts

    def _parse_outputs(self, outputs: list[str]) -> list[str]:
        return list(map(self.output_parser.parse, outputs))

    def _parse_last_assistant_output(self, output) -> list[str]:
        parse_output = output[0]["generated_text"][-1]["content"]
        return parse_output

    def _to_message(self, text: str) -> list[dict[str, str]]:
        messages = []
        if self.instruct:
            assistant = {"role": "assistant", "content": self.instruct}
            messages.append(assistant)
        user = {"role": "user", "content": text}
        messages.append(user)
        return messages