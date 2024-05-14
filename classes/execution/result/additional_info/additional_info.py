class AdditionalInfo:
    extent_relaxation: float
    similarity_function: list[str]
    comparison_operator: list[str]
    others: dict

    def __init__(self, extent_relaxation, similarity_function, comparison_operator, others):
        self.extent_relaxation = extent_relaxation
        self.similarity_function = similarity_function
        self.comparison_operator = comparison_operator
        self.others = others
        self.others = others