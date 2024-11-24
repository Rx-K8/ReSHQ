class SearchResult:
    def __init__(self, query: str, doc_id: str, content: str, score: float):
        self.query = query
        self.doc_id = doc_id
        self.content = content
        self.score = score
        self.rank = None

    def set_rank(self, rank: int):
        self.rank = rank

    def __str__(self):
        return f"SearchResult(query={self.query}, doc_id={self.doc_id}, content={self.content}, rank={self.rank}, score={self.score})"


class SearchResults:
    def __init__(self) -> None:
        self.search_results: list[SearchResult] = []
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.search_results):
            search_result = self.search_results[self.index]
            self.index += 1
            return search_result
        else:
            raise StopIteration

    def add_search_result(
        self, query: str, doc_id: str, content: str, score: float
    ):
        search_result = SearchResult(
            query,
            doc_id,
            content,
            score,
        )
        self.search_results.append(search_result)

    def sort(self):
        self.search_results.sort(key=lambda x: x.score, reverse=True)
        for i, search_result in enumerate(self.search_results):
            search_result.set_rank(i + 1)

    def to_validation(self, topic_id):
        self.sort()
        val_outputs = []
        for search_result in self.search_results:
            val_output = f"{topic_id} Q0 {search_result.doc_id} {search_result.rank} {search_result.score} Anserini"
            val_outputs.append(val_output)
        return val_outputs

    def __str__(self):
        return "\n".join(str(result) for result in self.search_results)
