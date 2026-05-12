# Flashcard: Math & Iteration

## Field: Front
How do you implement **Compounding Growth** and ensure the result is always a whole number?

## Field: Back
Use a **for loop** to repeat the math, and `math.floor()` to round down to the nearest integer.

**The Code**:
`import math`
`mp = mp + (mp * growth)`
`print(math.floor(mp))`

**Expert Prompt**:
"Create a function for **compounding growth**. Use a **for loop** to iterate 500 times, applying a 4.8% increase per step. Wrap the result in **math.floor** to keep values as integers."

## Field: Diagram
graph TD
    Start[Base MP: 10] --> Loop{For Level 1-100}
    Loop --> Math[Total = Total * 1.048]
    Math --> Floor[math.floor]
    Floor --> Result[Whole Number MP]
    Result --> Loop
