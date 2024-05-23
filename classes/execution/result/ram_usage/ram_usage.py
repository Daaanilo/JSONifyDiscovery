class RamUsage:
    unit: str
    max_ram_used: str

    def __init__(self, unit: str, max_ram_used: str):
        self.unit = unit
        self.max_ram_used = max_ram_used