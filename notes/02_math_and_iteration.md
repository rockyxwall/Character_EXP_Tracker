# Note 02: Math, Loops, and Formatting
*Based on MP_to_Mana.py and LEGACY_CODE_EXPLANATION.md*

### 1. Logic Breakdown
The "MP to Mana" logic is about **Compounding Growth**. It starts with a base value and increases it by a percentage (4.8%) over and over again for a certain number of steps (levels). It uses `math.floor` to keep the results as whole numbers.

### 2. Python Concepts
-   **`for k in range(2, 501):`**: A loop that repeats exactly 499 times.
-   **`math.floor()`**: Rounds a decimal *down* to the nearest whole number. Essential for RPGs where you can't have "0.5 mana."
-   **f-strings `f"MP{k} = {mana}"`**: A way to "inject" variables into text easily.
-   **Compounding Logic**: `total = total + (total * rate)`.

### 3. Why it Matters for Prompting
When asking an AI to build a progression system, specifying the **rounding method** and the **growth type** prevents bugs. If you just say "increase mana," the AI might use linear growth (always +5) instead of compounding growth (percentage based).

### 4. Prompt Example
> "Write a function to calculate Mana progression. It should take a `base_mp` and a `growth_rate`. Use a **for loop** to iterate up to 500. For each step, calculate the new total using **compounding growth**, and use **math.floor** to return only whole numbers. Output the result using an **f-string**."
