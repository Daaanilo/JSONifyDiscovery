class Attribute:
    column: str
    comparison_relaxation: float

    def __init__(self, column, comparison_relaxation):
        self.column = column
        self.comparison_relaxation = comparison_relaxation