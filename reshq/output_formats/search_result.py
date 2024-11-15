class SearchResult:
    def __init__(
        self, query: str, doc_id: str, content: str, rank: int, score: float
    ):
        self.query = query
        self.doc_id = doc_id
        self.content = content
        self.rank = rank
        self.score = score

    def __str__(self):
        return f"SearchResult(query={self.query}, doc_id={self.doc_id}, content={self.content}, rank={self.rank}, score={self.score})"


class SearchResults:
    def __init__(self) -> None:
        self.search_results: list[SearchResult] = []
        self.current_rank: int = 1
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
            self.current_rank,
            score,
        )
        self.search_results.append(search_result)
        self.increment_rank()

    def increment_rank(self):
        self.current_rank += 1

    def __str__(self):
        return "\n".join(str(result) for result in self.search_results)
