# Python Learning & AI Prompting (SVG Visual Edition)

This project focuses on understanding Python logic via **Visual Flashcards** that work everywhere (offline, mobile, web) using Inline SVGs.

## Workflow: Note to Flashcard
1.  **Write Note**: Create/edit a file in `notes/md/*.md` using the "Three-Field" structure (Front, Back, Diagram).
2.  **Generate SVGs**: Run `python notes/generate_diagrams.py`.
3.  **Import to Anki**: Import the generated `notes/flash-cards/_all_cards.txt` into Anki.

## Visual Flashcard Structure (`notes/md/*.md`)
-   **## Field: Front**: The question.
-   **## Field: Back**: Explanation, code, and prompting tips.
-   **## Field: Diagram**: Pure Mermaid syntax (for automatic SVG generation).

## Anki Setup (Method C - Inline SVG)
No add-ons or complex templates required!
- Create a Note Type with fields: `Front` and `Back`.
- Ensure your Anki Styling section has this to make SVGs look good:
```css
svg {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 10px auto;
}
```

## Prompting Principles
- **Logic-First**: Describe the behavior before asking for code.
- **Visual Mapping**: Use the Mermaid diagrams as a mental map for your AI instructions.
- **Explicit Constraints**: Always specify rounding (math.floor) and data types (Dictionaries vs Lists).
