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

# 4. Starting State (The "Level 1" defaults)
STARTING_LEVEL = 1
STARTING_EXP = 0
DEFAULT_STATS = {
    "STR": 10,
    "AGI": 10,
    "INT": 10,
    "VIT": 10
}

# 5. Folder Paths
CHAR_FOLDER = "characters"
MONSTER_FOLDER = "monsters"
