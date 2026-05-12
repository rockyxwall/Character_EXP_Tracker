# Python Learning & AI Prompting Guidelines

This project focuses on understanding Python logic to enable expert-level AI prompting. Use the `notes/` directory to document learnings.

## Note-Taking Structure
Every note in `notes/*.md` should follow this template to ensure clarity and utility for future AI prompting:

1.  **Logic Breakdown**: Explain *what* the code is doing in plain English (the "Business Logic").
2.  **Python Concept**: Identify the technical name (e.g., "List Comprehension", "Dataclass", "Dictionary").
3.  **Why it Matters for Prompting**: Explain how knowing this term helps you tell an AI exactly what to build.
4.  **Prompt Example**: A "Golden Prompt" snippet that uses the concept correctly.

## Prompting Principles
-   **Be Explicit about Data Structures**: Instead of "save the stats," say "store the stats in a dictionary with keys STR, VIT, and AGI."
-   **Define the Formula**: Don't just say "calculate EXP," say "calculate EXP using a quadratic formula: level squared times ten."
-   **Specify Validation**: Always tell the AI what to do if input is wrong (e.g., "If the user enters a non-number, catch the error and ask again").
-   **Logic First**: Describe the behavior before the code. "The system should prevent leveling up until a stat reaches 5."

## Directory Map
-   `legacy_code/`: Original scripts for analysis.
-   `notes/`: Educational breakdowns and prompting guides.
