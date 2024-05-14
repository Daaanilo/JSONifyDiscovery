class Algorithm:
    name: str
    language: str
    platform: str
    execution_type: str

    def __init__(self, name: str, language: str, platform: str, execution_type: str):
        self.name = name
        self.language = language
        self.platform = platform
        self.execution_type = execution_type
