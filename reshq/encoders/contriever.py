from transformers import AutoModel, AutoTokenizer

from reshq.similarity import dot_product


class Contriever:
    def __init__(self):
        self.model_id = "facebook/contriever"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModel.from_pretrained(self.model_id)

    def encode(self, sentences: str | list[str]):
        inputs = self.tokenizer(
            sentences, padding=True, truncation=True, return_tensors="pt"
        )
        outputs = self.model(**inputs)
        embeddings = self.mean_pooling(
            outputs.last_hidden_state, inputs["attention_mask"]
        )
        return embeddings

    def mean_pooling(self, token_embeddings, mask):
        token_embeddings = token_embeddings.masked_fill(
            ~mask[..., None].bool(), 0.0
        )
        sentence_embeddings = (
            token_embeddings.sum(dim=1) / mask.sum(dim=1)[..., None]
        )
        return sentence_embeddings

    def dot_score(self, sentence1, sentence2):
        embeddings = self.encode([sentence1, sentence2])
        return dot_product(embeddings[0], embeddings[1])
