'''
Constants
'''

from enum import IntEnum, auto
from dataclasses import dataclass

name_organisation = "leCacaonut"
name_program = "PerformanceMe"

default_icon_size = 60

images_play = 'images/play.png'
images_pause = 'images/pause.png'
images_plus = 'images/plus.png'
images_minus = 'images/minus.png'

stylesheet_light = 'stylesheets/light.qss'
stylesheet_dark = 'stylesheets/dark.qss'

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
