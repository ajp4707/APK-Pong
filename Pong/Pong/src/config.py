from enum import Enum

# -- Constants
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (150, 150, 150)
MUTEDGRAY = (79, 79, 79)

# -- Game properties
SCREENW = 1050  # In pixels
SCREENH = 750  
FPS = 60        # FPS for the game
WINSCORE = 21
SWITCHROUNDS = 5    # switch serves after how many rounds
TIMELIMIT = False   
MAXTIME = 185   # Only applied when TIMELIMIT = true

# -- Ball and paddle properties
BALLW = 15
BALLH = 15
VELOCITYMIN = 9
VELOCITYMAX = 14
SPEEDUPCTR = 4      # number of paddle hits or collisions before speed increases
PADW = 15
PADH = 75

# -- Serve Mechanic enums. Do not touch
class ServeType(Enum):
    STRAIGHT = 0
    WITHINBOUND = 1
    TWOSTEP = 2
    TOWARDCENTER = 3

# -- Serve Type for the game -> Please customize as needed
SERVETYPE = ServeType.TOWARDCENTER;
BOUNDRADIUS = 60 # number of pixels the "Bound" is from center of the screen
# ^^ only applies to WITHINBOUND serve type

# Minor adjustments
PAUSELENGTH = 1.5   # Seconds to pause after score, and before serve
COUNTFROM = 5      # Seconds of countdown before starting game
TEXTPAUSELENGTH = 3

SIZE = (SCREENW, SCREENH)


### Debug Constants for ease of access
### Comment out below when running for real
#WINSCORE = 10
SWITCHROUNDS = 2    # switch serves after how many rounds
#TIMELIMIT = False   
#MAXTIME = 185   # Only applied when TIMELIMIT = true

## Minor adjustments
#PAUSELENGTH = 1.5   # Seconds to pause after score, and before serve
COUNTFROM = 0      # Seconds of countdown before starting game
TEXTPAUSELENGTH = 0.5
