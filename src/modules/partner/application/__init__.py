import importlib
from lato import ApplicationModule

partner_module = ApplicationModule("Partner")
importlib.import_module("src.modules.partner.application.commands")
importlib.import_module("src.modules.partner.application.queries")
importlib.import_module("src.modules.partner.application.events")