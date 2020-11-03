'''
Constants
'''

from enum import Enum, IntEnum, auto
from dataclasses import dataclass



default_icon_size = 75
data_filename = '/userdata'
settings_fileName = '/settings'

class Name(str, Enum):
    organisation = "leCacaonut"
    program = "PerformanceMe"

class Stylesheets(str, Enum):
    light_theme = 'stylesheets/light.qss'
    dark_theme = 'stylesheets/dark.qss'

class Images(str, Enum):
    play = 'images/play.png'
    pause = 'images/pause.png'
    plus = 'images/plus.png'
    minus = 'images/minus.png'
    exit = 'images/exit.png'
    switch = 'images/switch.png'

class ActionType(IntEnum):
    appraisal = auto()
    listing = auto()
    sale = auto()

class PushButtons(IntEnum):
    calls_minus = auto()
    calls_plus = auto()
    connects_minus = auto()
    connects_plus = auto()
    BAP_minus = auto()
    BAP_plus = auto()
    MAP_minus = auto()
    MAP_plus = auto()
    LAP_minus = auto()
    LAP_plus = auto()

@dataclass
class Tally:
    calls = 0
    connects = 0
    BAP = 0
    MAP = 0
    LAP = 0
