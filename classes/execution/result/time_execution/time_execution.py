class TimeExecution:
    unit: str  #inserire enumerazione
    dataset_loading: str
    preprocessing: str
    discovery: str
    total: str
    others: dict

    def __init__(self, unit: str, dataset_loading: str, preprocessing: str, discovery: str, total: str, others: dict):
        self.unit = unit
        self.dataset_loading = dataset_loading
        self.preprocessing = preprocessing
        self.discovery = discovery
        self.total = total
        self.others = others
