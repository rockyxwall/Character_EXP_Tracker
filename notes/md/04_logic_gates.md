# Flashcard: Logic Gates

## Field: Front
How do you prevent a function from running unless a specific condition is met?

## Field: Back
Use a **Validation Gate** with a conditional `if` and an early `return`.

**The Code**:
`def can_gain_exp(self):`
`    return any(v >= 5 for v in self.stats.values())`
`if not self.can_gain_exp(): return`

**Expert Prompt**:
"Add a **validation gate** to the EXP method. Use **any()** to check if any stat value is 5 or higher. If not, **return early** without granting EXP."

## Field: Diagram
flowchart TD
    Start[Gain EXP] --> Check{"Any Stat >= 5?"}
    Check -- No --> Fail[Return: Stop]
    Check -- Yes --> Logic[Calculate EXP]
    Logic --> End[Level Up]
