# Note 03: Classes and Dataclasses
*Based on Tristan_EXP_Tracker.py and Full.py*

### 1. Logic Breakdown
A "Character" isn't just one variable; it's a collection of data (Name, Level, EXP) and actions (Gain EXP, Level Up). Instead of having loose variables everywhere, we wrap them into a "Class." 

### 2. Python Concepts
-   **`class Character:`**: A blueprint for creating "objects."
-   **`self`**: A way for the character to refer to its own data (like `self.level`).
-   **`__init__`**: The "Setup" function that runs when a character is first created.
-   **`@dataclass`**: A modern, shortcut way to write classes (seen in `Full.py`) that handles the setup automatically.
-   **Methods**: Functions *inside* a class, like `gain_exp()`.

### 3. Why it Matters for Prompting
This is the "Expert" level. Instead of asking for a "script to track exp," you ask for a "Character **Class**." This makes the code modular. You can have 10 different "Character objects" running at once without the data getting mixed up.

### 4. Prompt Example
> "Create a Python **Dataclass** named `Character`. It should have attributes for `name`, `level`, and `current_exp`. Add a **method** called `gain_exp` that handles the logic for leveling up when `current_exp` exceeds a `threshold` formula. Ensure the **method** updates `self.level` and resets `self.current_exp`."
