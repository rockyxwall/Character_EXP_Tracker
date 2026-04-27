#!/usr/bin/env python3
import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# ----------------------------
# Constants & Config
# ----------------------------
STATS = ("STR", "VIT", "AGI", "DEX", "MNA")  # INT & LUC removed
MP_GROWTH_RATE = 0.048  # 4.8%
def EXP_FORMULA(lvl): return lvl ** 2 * 10
def THRESHOLD(lvl): return lvl * 5


ROLE_PRESETS = {
    "adventurer": {"STR": 6, "AGI": 6, "VIT": 4, "DEX": 4, "MNA": 3},
    "paladin": {"STR": 7, "VIT": 8, "AGI": 3, "DEX": 3, "MNA": 2},
    "merchant": {"STR": 3, "VIT": 4, "AGI": 3, "DEX": 4, "MNA": 2},
    "scholar": {"STR": 2, "VIT": 3, "AGI": 2, "DEX": 3, "MNA": 8},
    "rogue": {"STR": 4, "VIT": 3, "AGI": 9, "DEX": 7, "MNA": 2},
    "soldier": {"STR": 8, "VIT": 7, "AGI": 4, "DEX": 3, "MNA": 1},
    "ranger": {"STR": 5, "VIT": 4, "AGI": 7, "DEX": 8, "MNA": 2},
    "mage": {"STR": 2, "VIT": 3, "AGI": 3, "DEX": 3, "MNA": 10},
}

KEYWORD_STAT_BONUSES = {
    "swordsman": ("STR", 12), "marathon": ("VIT", 10), "archer": ("DEX", 10),
    "mage": ("MNA", 12),
    "wizard": ("MNA", 14), "blacksmith": ("STR", 8),
    "one-man-army": ("STR", 14),
    "paladin": ("VIT", 8), "adventurer": ("AGI", 4)
}


def age_baseline(age: int) -> Dict[str, int]:
    if age is None:
        return {k: 5 for k in STATS}
    if age < 18:
        return {"STR": 5, "VIT": 5, "AGI": 6, "DEX": 5, "MNA": 4}
    if age < 30:
        return {"STR": 8, "VIT": 8, "AGI": 8, "DEX": 8, "MNA": 6}
    if age < 45:
        return {"STR": 9, "VIT": 10, "AGI": 7, "DEX": 8, "MNA": 8}
    return {"STR": 7, "VIT": 9, "AGI": 6, "DEX": 7, "MNA": 7}

# ----------------------------
# Character Class
# ----------------------------


@dataclass
class Character:
    name: str
    race: str = "Human"
    level: int = 1
    current_exp: int = 0
    exp_to_next: int = field(init=False)
    stats: Dict[str, int] = field(
        default_factory=lambda: {k: 0 for k in STATS})
    mp: int = 10
    skills: List[str] = field(default_factory=list)
    titles: List[str] = field(default_factory=list)
    gift: str = ""

    def __post_init__(self):
        self.exp_to_next = EXP_FORMULA(self.level)

    def seed_from(self, age: int = None, role: str = None, keywords: List[str] = None):
        base = age_baseline(age)
        for k, v in base.items():
            self.stats[k] += v

        if role:
            preset = ROLE_PRESETS.get(role.lower())
            if preset:
                for k, bonus in preset.items():
                    rnd = random.randint(-2, 3)
                    self.stats[k] += max(0, bonus + rnd)

        if keywords:
            for kw in keywords:
                if not kw:
                    continue
                ent = KEYWORD_STAT_BONUSES.get(kw.lower())
                if ent:
                    stat, bonus = ent
                    self.stats[stat] += bonus

        for s in STATS:
            self.stats[s] += random.randint(0, 3)

    def can_gain_exp(self) -> bool:
        if self.level != 1:
            return True
        return any(v >= 5 for v in self.stats.values())

    def exp_gain_multiplier(self, monster_level: int) -> float:
        diff = monster_level - self.level
        mult = 1.0 + 0.2 * diff
        return mult if mult > 0 else 0.0

    def monster_base_exp(self, monster_level: int) -> int:
        return math.floor((monster_level ** 2 * 10) * 0.1)

    def bump_highest_stat_to_threshold(self):
        need = THRESHOLD(self.level)
        top = max(self.stats.items(), key=lambda kv: kv[1])[0]
        if self.stats[top] < need:
            self.stats[top] = need

    # ----------------------------
    # Updated Level-Up Rules
    # ----------------------------
    def gain_exp_from_batch(self, monster_level: int, quantity: int, verbose: bool = True):
        base_exp = self.monster_base_exp(monster_level)
        if verbose:
            print(
                f"\nProcessing {quantity} x Monster Lv {monster_level} | Base EXP per kill: {base_exp}")

        for kill in range(1, quantity + 1):
            if not self.can_gain_exp():
                if verbose:
                    print(
                        f"Kill #{kill}: No EXP gained. Level-1 gate not met.")
                continue

            mult = self.exp_gain_multiplier(monster_level)
            gained = math.floor(base_exp * mult)
            prev_level = self.level

            self.current_exp += gained
            while self.current_exp >= self.exp_to_next:
                self.current_exp -= self.exp_to_next
                self.level += 1
                self.exp_to_next = EXP_FORMULA(self.level)

                # Highest stat bump
                need = THRESHOLD(self.level)
                top_stat = max(self.stats.items(), key=lambda kv: kv[1])[0]
                if self.stats[top_stat] < need:
                    self.stats[top_stat] = need

                # All other stats +1 every level
                # for stat in STATS:
                #     if stat != top_stat:
                #         self.stats[stat] += 1

                # if verbose:
                #     print(
                #         f"Kill #{kill} Level Up! Level {prev_level} -> {self.level} | Carryover {self.current_exp} EXP")

            if verbose:
                print(
                    f"Kill #{kill}: Level {prev_level} -> Level {self.level} | Gained {gained} EXP")

    # ----------------------------
    # MP Growth based on MNA
    # ----------------------------
    def mp_growth_table(self, base_mp: float = None) -> Tuple[List[Tuple[int, int, int, str]], int]:
        if base_mp is None:
            base_mp = float(self.mp)
        mp_total = float(base_mp)
        upto = max(1, self.stats.get("MNA", 1))
        rows: List[Tuple[int, int, int, str]] = [
            (1, math.floor(mp_total), 0, f"MP1 = {base_mp}")]
        for k in range(2, upto + 1):
            prev = mp_total
            mp_total = prev + prev * MP_GROWTH_RATE
            floored_total = math.floor(mp_total)
            floored_prev = math.floor(prev)
            increase = floored_total - floored_prev
            formula = f"[{prev:.6f} + ({prev:.6f} x {MP_GROWTH_RATE*100:.2f}%)]"
            rows.append((k, floored_total, increase, formula))
        return rows, math.floor(mp_total)

    def print_sheet(self, show_mp_total: int = None):
        print("\nFinal Character Sheet:")
        print(f"Name: {self.name}")
        print(f"Race: {self.race}")
        print(f"Lv: {self.level} ({self.current_exp}/{self.exp_to_next})")
        print("Status:")
        if show_mp_total:
            print(f"MP: {show_mp_total}")
        else:
            print(f"MP: {self.mp}")
        for s in STATS:
            print(f"{s}: {self.stats[s]}")
        if self.skills:
            print("Skills:", self.skills)
        if self.titles:
            print("Titles:", self.titles)
        if self.gift:
            print("Gift:", self.gift)

# ----------------------------
# Driver / CLI
# ----------------------------


def input_with_blank(prompt: str):
    v = input(prompt).strip()
    return v if v != "" else None


def main():
    random.seed()
    print("Enter character info (leave blank if unknown):")
    name = input_with_blank("Name: ") or "Unknown"
    age_raw = input_with_blank("Age (number): ")
    age = int(age_raw) if age_raw else None
    role = input_with_blank(
        "Role (Adventurer/Paladin/Merchant/Scholar/Rogue/Soldier/Ranger/Mage): ")
    keywords_raw = input_with_blank(
        "Keywords (comma separated, e.g., swordsman, mage): ")
    keywords = [k.strip()
                for k in keywords_raw.split(",")] if keywords_raw else []

    player = Character(name=name, race="Human")
    player.seed_from(age=age, role=role, keywords=keywords)

    skills_raw = input_with_blank("Skills (comma separated, cosmetic): ")
    if skills_raw:
        player.skills = [s.strip() for s in skills_raw.split(",")]
    titles_raw = input_with_blank("Titles (comma separated, cosmetic): ")
    if titles_raw:
        player.titles = [t.strip() for t in titles_raw.split(",")]
    gift_raw = input_with_blank("Gift (single word, cosmetic): ")
    if gift_raw:
        player.gift = gift_raw

    base_mp_raw = input_with_blank(
        "Base MP (leave blank to use current MP=10): ")
    if base_mp_raw:
        try:
            player.mp = int(base_mp_raw)
        except:
            player.mp = float(base_mp_raw) if "." in base_mp_raw else player.mp

    # Monster batch input
    print("\nEnter monster batches. Format: Name Level Quantity. Type 'done' when finished.")
    monsters: List[Tuple[str, int, int]] = []
    while True:
        raw = input(
            "Enter monster as 'Name Level Quantity' or 'done': ").strip()
        if raw.lower() == "done":
            break
        parts = raw.split()
        if len(parts) < 3:
            print("Invalid format. Example: dragon 30 1")
            continue
        try:
            m_name = parts[0]
            m_level = int(parts[1])
            qty = int(parts[2])
            monsters.append((m_name, m_level, qty))
        except Exception:
            print("Invalid numbers. Example: dragon 30 1")
            continue

    for m_name, m_level, qty in monsters:
        player.gain_exp_from_batch(m_level, qty, verbose=True)

    table, total_mp = player.mp_growth_table(base_mp=float(player.mp))
    print("\nMP Growth according to MNA:")
    for mp_num, mana, inc, formula in table:
        print(f"MP{mp_num} = {mana} mana, increase = {inc}, calc: {formula}")
    print(f"Total Mana at MP{player.stats['MNA']} = {total_mp}")

    player.print_sheet(show_mp_total=total_mp)


if __name__ == "__main__":
    main()


