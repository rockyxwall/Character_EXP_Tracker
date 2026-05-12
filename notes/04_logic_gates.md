# Note 04: Advanced Logic and "Gates"
*Based on Full.py*

### 1. Logic Breakdown
`Full.py` contains "Gates." For example, the `can_gain_exp` function checks if a character is "Level 1" and if they have any stat >= 5. If not, they gain 0 EXP. This is "Conditional Validation."

### 2. Python Concepts
-   **`any()`**: Returns True if *any* item in a list meets a condition. Great for "Check if any stat is high enough."
-   **`max(stats.items(), key=...)`**: A fancy way to find which stat is the highest.
-   **Conditional Gates**: `if not self.can_gain_exp(): continue`. This skips the rest of the logic.

### 3. Why it Matters for Prompting
AI often writes "happy path" code (it assumes everything works). You need to prompt for "Edge Cases" and "Validation Gates." Knowing how to describe these gates makes your software robust.

### 4. Prompt Example
> "In the `gain_exp` method, add a **validation gate**. If the character is level 1, they should only gain EXP if **any** of their stats are greater than or equal to 5. Use the **any()** function for this check. If the check fails, print a warning and **return** early."
