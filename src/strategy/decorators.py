from .strategy_status import StrategyStatus

def check_status_is_not_discontinued(method):
    def wrapper(self, *args, **kwargs):
        assert self.status != StrategyStatus.DISCONTINUED, "Strategy is discontinued. You must change the status."
        result = method(self, *args, **kwargs)
        return result
    return wrapper