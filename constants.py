"""Constants"""


from enum import Enum, IntEnum, auto
from dataclasses import dataclass


default_icon_size = 75
data_file_name = '/userdata'
data_file_extension = '.json'
settings_file_name = '/settings.perfme'

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
    hamburger = 'images/hamburger.png'

class ActionType(IntEnum):
    appraisal = auto()
    listing = auto()
    sale = auto()

class SortType(IntEnum):
    date = auto()
    suburb = auto()
    street = auto()
    number = auto()

class TimerPushButtons(IntEnum):
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

motivational_string = """
    <u><b><i>YOU SET YOUR GOAL TO ZERO</i></b></u> <p> Nothing in life is worthwhile...unless you take <i>risks</i>. 
    <b>Nothing</b>. There is no passion to be found playing <i>small</i>, and settling for a life that's <i>less</i>
    than the one you're <i>capable of living</i>.</p><p> Don't be afraid to <b>fail big</b>...to <b>dream big</b>. 
    <br> But remember, dreams without <b><i>GOALS</i></b> are just <b>dreams</b>...</p>
"""
shortcut_help = """
Hotkeys
    Dashboard:
        a:      add appraisal
        l:      add listing
        s:      add sale
        g:      set goals
    Timer:
        s:          set timer
        spacebar:   start/pause timer
        1-5:        add tally
        shift 1-5:  remove tally
    Details:
        comma:      sorting method
        period:     sort ascending/descending
"""