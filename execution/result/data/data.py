from classes.execution.result.data.attribute import Attribute

class Data:
    rhs: Attribute
    lhs: list[Attribute]
    cc: str

    def __init__(self, rhs: Attribute, lhs: list[Attribute], cc: str):
        self.rhs = rhs
        self.lhs = lhs
        self.cc = cc