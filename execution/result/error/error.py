class Error:
    time_limit: str
    memory_limit: str
    general_error: str

    def __init__(self, time_limit: str, memory_limit: str, general_error: str):
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.general_error = general_error