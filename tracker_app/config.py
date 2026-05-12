# --- TRACKER CONFIGURATION ---

# 1. Keywords (Author can change these to 'k', 'g', 'defeted', etc.)
KEYWORDS = {
    "KILL": ["Killed", "k", "d", "defeated", "slain"],
    "GAIN": ["Gain", "g", "reward", "exp+", "gexp"],
}


# 2. Stat Settings
# This pattern finds things like "STR: 10" or "AGI: 5"
STAT_PATTERN = r"([A-Z]{2,3}):\s*(\d+)" 

# 3. UI Settings
BAR_CHAR_FILLED = "="
BAR_CHAR_EMPTY = "-"
BAR_LENGTH = 15
WINDOW_WIDTH = 40
HEADER_TEXT = "[ STATUS WINDOW ]"

# 4. Folder Paths
CHAR_FOLDER = "characters"
MONSTER_FOLDER = "monsters"

# 5. Status Block Header
STATUS_HEADER = "## [ CURRENT STATUS ]"
