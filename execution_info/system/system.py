class System:
    os: str
    os_version: str
    processor: str
    thread: str
    core: str
    ram: str

    def __init__(self, os: str, os_version: str, processor: str, thread: str, core: str, ram: str):
        self.os = os
        self.os_version = os_version
        self.processor = processor
        self.thread = thread
        self.core = core
        self.ram = ram