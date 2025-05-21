class StrategyError(Exception):
    def __init__(self, message: str = "Strategy domain error"):
        super().__init__(self, message)

class TermNotFound(StrategyError):
    ...    
