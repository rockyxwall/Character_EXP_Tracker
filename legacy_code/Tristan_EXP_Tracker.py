import math


class Character:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.current_exp = 0
        self.exp_to_next = self.level ** 2 * 10

    def exp_gain_multiplier(self, monster_level):
        diff = monster_level - self.level
        multiplier = 1.0 + 0.2 * diff
        if multiplier < 0:
            multiplier = 0.0
        return multiplier

    def gain_exp(self, monster_level, quantity):
        base_exp = math.floor((monster_level ** 2 * 10) * 0.1)
        print(
            f"\nProcessing {quantity} x Monster Lv {monster_level} | Base EXP per kill: {base_exp}")

        for kill in range(1, quantity + 1):
            multiplier = self.exp_gain_multiplier(monster_level)
            raw_exp = base_exp * multiplier
            gained_exp = math.floor(raw_exp)
            prev_level = self.level
            prev_exp = self.current_exp

            self.current_exp += gained_exp

            # Handle level-ups
            while self.current_exp >= self.exp_to_next:
                self.current_exp -= self.exp_to_next
                self.level += 1
                self.exp_to_next = self.level ** 2 * 10
                print(
                    f"Kill #{kill} Level Up! Level {prev_level} -> {self.level} | [Carryover {self.current_exp} Exp]")

            print(f"Kill #{kill}: Level {prev_level} ({prev_exp}/{prev_level**2*10}) -> "
                  f"Level {self.level} ({self.current_exp}/{self.exp_to_next}) | [Gained {gained_exp} Exp]")


def main():
    name = "Tristan"
    player = Character(name)

    monsters = []
    while True:
        monster_input = input(
            "\nEnter monster in format 'Name Level Quantity' or 'done' to finish: ")
        if monster_input.lower() == "done":
            break
        try:
            parts = monster_input.split()
            monster_name = parts[0]
            monster_level = int(parts[1])
            quantity = int(parts[2])
            monsters.append((monster_name, monster_level, quantity))
        except:
            print(
                "Invalid format. Please use 'Name Level Quantity', e.g., HornedRabbit 4 87")
            continue

    # Process monsters
    for m_name, m_level, m_qty in monsters:
        player.gain_exp(m_level, m_qty)

    print(f"\nFinal Character Sheet:")
    print(f"Name: {player.name}")
    print(f"Level: {player.level} ({player.current_exp}/{player.exp_to_next})")
    # print(f"EXP: {player.current_exp}/{player.exp_to_next}")


if __name__ == "__main__":
    main()


