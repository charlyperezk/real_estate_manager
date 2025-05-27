import importlib
from lato import ApplicationModule

operation_module = ApplicationModule("Operation")
importlib.import_module("src.modules.operation.application.commands")
importlib.import_module("src.modules.operation.application.queries")
importlib.import_module("src.modules.operation.application.events")