import importlib
from lato import ApplicationModule

strategy_module = ApplicationModule("Strategy")
importlib.import_module("src.modules.strategy.application.commands")
importlib.import_module("src.modules.strategy.application.queries")
importlib.import_module("src.modules.strategy.application.events")