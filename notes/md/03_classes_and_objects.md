# Flashcard: Classes & Dataclasses

## Field: Front
What is a "Blueprint" in Python used to group data and actions together?

## Field: Back
A **Class** (or **Dataclass**) bundles data and functions (methods) into a single "Object."

**The Code**:
`@dataclass`
`class Character:`
`    def gain_exp(self, amount):`

**Expert Prompt**:
"Design a **Python Dataclass** called `Character` with attributes for `name` and `level`. Include a **method** inside the class to handle EXP gain logic."

## Field: Diagram
classDiagram
    class Character {
        +String name
        +int level
        +int current_exp
        +gain_exp(amount)
        +level_up()
    }
