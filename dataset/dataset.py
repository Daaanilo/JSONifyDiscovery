class Dataset:
    name: str
    header: list[str]
    size: str
    format: str
    col_number: str
    row_number: str
    separator: str
    blank_char: str

    def __init__(self, name: str, header: list[str], size: str, format: str, col_number: str, row_number: str, separator: str, blank_char: str):
        self.name = name
        self.header = header
        self.size = size
        self.format = format
        self.col_number = col_number
        self.row_number = row_number
        self.separator = separator
        self.blank_char = blank_char
