from typing import Optional

from transformers import pipeline

from reshq.language_models.base import BaseLanguageModel
from reshq.output_parsers.base import BaseOutputParser


class LanguageModel(BaseLanguageModel):
    """
    LanguageModel is a class for generating text using a pre-trained language model.

    Args:
        model_id (str): The identifier of the pre-trained model to use.
        output_parser (Optional[BaseOutputParser]): An optional parser to process the model's output.
        instruct (Optional[str]): An optional instruction to guide the model's generation.

    Attributes:
        generator (pipeline): The text generation pipeline from the transformers library.
        output_parser (Optional[BaseOutputParser]): The parser to process the model's output.
        instruct (Optional[dict[str, str]]): The instruction to guide the model's generation.

    Methods:
        generate(texts: list[str] | str) -> list[str]:
            Generates text based on the input texts.

        _create_prompts(texts: list[str]) -> list[list[dict[str, str]]]:
            Creates prompts for the model based on the input texts.

        _ensure_list(texts: list[str] | str) -> list[str]:
            Ensures the input is a list of strings.

        _parse_outputs(outputs: list[str]) -> list[str]:
            Parses the model's outputs using the output parser.

        _parse_last_assistant_output(output) -> list[str]:
            Parses the last assistant output from the model's generated text.

        _to_message(text: str) -> list[dict[str, str]]:
            Converts a text string into a message format for the model.
    """

    def __init__(
        self,
        model_id: str,
        output_parser: Optional[BaseOutputParser] = None,
        instruct: Optional[str] = None,
        batch_size: int = 8,
    ):
        self.generator = pipeline("text-generation", model=model_id, device_map="auto")
        self.output_parser = output_parser
        self.instruct: Optional[dict[str, str]] = (
            {"role": "assistant", "content": instruct} if instruct else None
        )
        self.batch_size = batch_size

    def generate(self, texts: list[str] | str) -> list[str]:
        texts = self._ensure_list(texts)
        texts = [self.clip_text(text) for text in texts]

        prompts = self._create_prompts(texts)
        outputs_with_context = self.generator(prompts, batch_size=self.batch_size)
        outputs = list(
            map(self._parse_last_assistant_output, outputs_with_context)
        )
        if self.output_parser:
            outputs = self._parse_outputs(outputs)

        return outputs

    def clip_text(self, text):
        if len(text) > 7000:
            text = text[:7000]
        return text

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
