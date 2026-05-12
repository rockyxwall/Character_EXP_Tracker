# Legacy Code Explanation: RPG Mechanics & Formulas

This document outlines the core mathematical models and RPG progression systems extracted from the legacy scripts in `legacy_code/`.

## 1. Experience (EXP) & Leveling
The leveling system uses a quadratic curve for requirements and a linear scaling multiplier for monster encounters.

- **EXP to Next Level**: 
  `Requirement = Level^2 * 10`
- **Monster Base EXP**: 
  `Base = floor((Monster_Level^2 * 10) * 0.1)`
- **EXP Multiplier**: 
  `Multiplier = 1.0 + 0.2 * (Monster_Level - Player_Level)`
  *(Note: The multiplier is clamped to a minimum of 0. Total EXP = Base * Multiplier)*

## 2. Stat Progression
### Automatic Stat Bumps
Upon leveling up, the character's highest primary stat is compared against a level-based threshold.
- **Rule**: If the highest stat is below `Level * 5`, it is automatically set to `Level * 5`.

### MP (Mana Points) Growth
MP growth is heavily dependent on the **MNA** (Mana/Magic) stat.
- **Formula**: For every point allocated to MNA, the base MP compounds by **4.8%**.
  `MP_new = MP_prev + (MP_prev * 0.048)`

## 3. Character Initialization
Initial stats are determined by a combination of Age, Role, and Keywords.

- **Age**: Stats are initialized based on life stages (e.g., Youth < 18, Adult < 30, Middle Age < 45).
- **Roles**: Fixed bonuses applied to specific stats (e.g., Paladin, Adventurer).
- **Keywords**: Semantic identifiers that provide flat stat bonuses (e.g., `swordsman` adds +12 to Strength).

## 4. Energy Progression (ENP) Prototypes
*Note: These formulas were extracted from experimental scripts (`mana_test1.py`, `test2.py`, `test3.py`) during cleanup.*

### Soft Cap Model (Diminishing Returns)
Designed to approach a limit of 5000.
- **Formula**: `ENP = prev + (5000 - prev) * (growth_rate / 100.0)`

### Compounding Decaying Growth
Growth that slows down as the level increases.
- **Formula**: `ENP = prev + prev * (growth_rate / 100)`
- **Decay**: The `growth_rate` decreases periodically (e.g., a 1.0% or 0.4% reduction every 10 levels).

---
*Documented on April 27, 2026*
