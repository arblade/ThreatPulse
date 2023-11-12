from .checkpointresearch import CheckPointResearchHandler
from .analyst1 import Analyst1Handler
from .bleepingcomputer import BleepingComputer
from .sekoia import SekoiaHandler
from .cisa_alerts import CISAAlertsHandler
from .redcanary import RedCanaryBlogHandler

HANDLERS = [CheckPointResearchHandler, Analyst1Handler, BleepingComputer, SekoiaHandler, CISAAlertsHandler, RedCanaryBlogHandler]