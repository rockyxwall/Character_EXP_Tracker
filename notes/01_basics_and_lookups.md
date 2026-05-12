# Note 01: Lists, Dictionaries, and User Input
*Based on L01.py and MP_to_Mana.py*

### 1. Logic Breakdown
The code shows how to present a list of choices (Roles and Keywords) to a user, take their numeric input, and map that number back to a specific name. It also shows how to store "bonuses" (like `swordsman` = +12 STR) in a lookup table.

### 2. Python Concepts
-   **List `[]`**: An ordered collection. `ROLE_PRESETS = ["adventurer", "paladin"]`.
-   **Dictionary `{}`**: A map of keys to values. `STATS = {"STR": 5, "VIT": 5}`. This is perfect for "Lookups."
-   **`enumerate()`**: A tool that goes through a list and gives you both the index (number) and the item.
-   **`int(input())`**: Taking a string from the user and turning it into a number so you can do math or use it as an index.

### 3. Why it Matters for Prompting
If you don't know these terms, you might ask an AI to "make a list of roles." The AI might give you a simple list. If you say, "Store roles in a **Dictionary** where the key is the role name and the value is a **Dictionary** of stat bonuses," the AI will write much more powerful and organized code.

### 4. Prompt Example
> "Create a Python script that stores RPG classes in a **dictionary**. Each class should have a nested dictionary for 'base_stats'. Use a **loop** with **enumerate** to display these as a numbered menu for the user, and use **int(input)** to capture their selection."
