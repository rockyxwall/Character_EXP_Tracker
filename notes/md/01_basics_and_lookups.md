# Flashcard: Basics & Lookups

## Field: Front
What is the best Python data structure for mapping a "Key" to a "Value", and how do you loop with numbers?

## Field: Back
Use a **Dictionary** for mapping and **enumerate** to turn lists into numbered menus.

**The Code**:
`ROLE_BONUS = {"paladin": {"STR": 7}}`
`for i, name in enumerate(roles, 1):`

**Expert Prompt**:
"Store RPG classes in a **dictionary** mapping names to stat-bonus dictionaries. Use a **for loop** with **enumerate** to display a numbered selection menu."

## Field: Diagram
graph LR
    Input[User Input: 1] --> Menu[Enumerate List]
    Menu --> Key[Role Name: Paladin]
    Key --> Lookup{Dictionary}
    Lookup --> Bonus1[STR: +7]
    Lookup --> Bonus2[VIT: +8]
