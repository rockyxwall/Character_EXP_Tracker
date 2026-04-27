ROLE_PRESETS = [
    "adventurer",
    "paladin",
    "merchant",
    "scholar",
    "rogue",
    "soldier",
    "ranger",
    "mage",
]

KEYWORDS = [
    "swordsman",
    "mage",
    "wizard",
    "one-man-army",
    "paladin",
    "adventurer"
]

print(f"Chosse Your Role")
for list_int, roles in enumerate(ROLE_PRESETS, start=1):
    print(f"{list_int}. {roles.capitalize()}")

choice_role = int(input("Chose your role: "))
role_index_int = ROLE_PRESETS[choice_role - 1].capitalize()

print(f"Chosse Your Keywords")
for list_int, keywords in enumerate(KEYWORDS, start=1):
    print(f"{list_int}. {keywords.capitalize()}")

choice_keyword = int(input("Chose your Keyword: "))
keyword_index_int = KEYWORDS[choice_keyword - 1].capitalize()

if 1 <= choice_role <= len(ROLE_PRESETS):
    print(f"Your Role Is:", role_index_int)
else:
    print("try again")

if 1 <= choice_keyword <= len(ROLE_PRESETS):
    print(f"Your Keyword Is:", keyword_index_int)
else:
    print("try again")


