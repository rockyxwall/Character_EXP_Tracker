import re
import math
import time
from pathlib import Path
import config

class Character:
    def __init__(self, file_path):
        self.path = Path(file_path)
        self.reset()
        self.load_and_process()

    def reset(self):
        self.name = "Unknown"
        self.level = config.STARTING_LEVEL
        self.exp = config.STARTING_EXP
        self.exp_needed = self.level ** 2 * 100
        self.stats = config.DEFAULT_STATS.copy()

    def load_and_process(self):
        try:
            self.content = self.path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"ERROR: Failed to read {self.path.name} -> {e}", flush=True)
            return

        name_match = re.search(r"# Name:\s*(.*)", self.content)
        if name_match: self.name = name_match.group(1).strip()

        log_section = re.search(r"## Log\s*\n(.*?)(?=\n##|$)", self.content, re.DOTALL)
        if log_section:
            kill_words = "|".join(config.KEYWORDS["KILL"])
            gain_words = "|".join(config.KEYWORDS["GAIN"])
            
            actions = log_section.group(1).strip().split('\n')
            for action in actions:
                action = action.strip()
                if not action: continue

                s_match = re.search(r"([A-Z]{2,3})\s*([+-]\d+)", action)
                if s_match:
                    self.modify_stat(s_match.group(1).upper(), int(s_match.group(2)))
                    continue

                action_pattern = rf"({kill_words}|{gain_words}):"
                type_match = re.search(rf"{action_pattern}\s*(.*?)(?:\s+[x*](\d+))?$", action, re.IGNORECASE)
                
                if type_match:
                    raw_type = type_match.group(1).lower().rstrip(':')
                    val = type_match.group(2).strip()
                    qty = int(type_match.group(3)) if type_match.group(3) else 1
                    
                    if any(raw_type == k.lower() for k in config.KEYWORDS["KILL"]):
                        self.gain_exp(val, qty)
                    elif any(raw_type == g.lower() for g in config.KEYWORDS["GAIN"]):
                        try:
                            self.add_raw_exp(int(val) * qty)
                        except ValueError:
                            print(f"ERR: Invalid gain value '{val}'", flush=True)
                else:
                    # Only print if not a known action and not empty
                    if action.strip() and not action.startswith('#'):
                        print(f"SKIP: {action}", flush=True)

    def save(self):
        new_content = self.content
        new_content = re.sub(r"Level:\s*\d+", f"Level: {self.level}", new_content)
        new_content = re.sub(r"EXP:\s*\d+/\d+", f"EXP: {self.exp}/{self.exp_needed}", new_content)
        for stat, val in self.stats.items():
            new_content = re.sub(rf"{stat}:\s*\d+", f"{stat}: {val}", new_content)

        if new_content != self.content:
            try:
                self.path.write_text(new_content, encoding='utf-8')
                self.content = new_content
                return True
            except Exception as e:
                print(f"ERR: Save failed {self.path.name} -> {e}", flush=True)
        return False

    def modify_stat(self, stat_name, mod):
        if stat_name in self.stats:
            self.stats[stat_name] += mod

    def add_raw_exp(self, amount):
        self.exp += amount
        self._check_level_up()

    def gain_exp(self, monster_name, qty):
        monster_file = Path(config.MONSTER_FOLDER) / f"{monster_name.replace(' ', '')}.md"
        if not monster_file.exists():
            print(f"ERR: Missing monster file {monster_file.name}", flush=True)
            return
        
        m_content = monster_file.read_text(encoding='utf-8')
        m_lvl = int(re.search(r"Level:\s*(\d+)", m_content).group(1))
        m_reward = int(re.search(r"EXP_Reward:\s*(\d+)", m_content).group(1))
        
        for _ in range(qty):
            multiplier = max(0, 1 + (m_lvl - self.level) * 0.2)
            self.exp += math.floor(m_reward * multiplier)
            self._check_level_up()

    def _check_level_up(self):
        while self.exp >= self.exp_needed:
            self.exp -= self.exp_needed
            self.level += 1
            self.exp_needed = self.level ** 2 * 100

def main():
    print(f"SYSTEM: Monitoring {config.CHAR_FOLDER}/", flush=True)
    char_folder = Path(config.CHAR_FOLDER)
    last_mtimes = {}

    while True:
        try:
            for char_file in char_folder.glob("*.md"):
                current_mtime = char_file.stat().st_mtime
                if char_file not in last_mtimes or current_mtime > last_mtimes[char_file]:
                    char = Character(char_file)
                    if char.save():
                        print(f"UPDATED: {char.name} (Lv {char.level})", flush=True)
                    last_mtimes[char_file] = char_file.stat().st_mtime
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nSYSTEM: Stopping tracker", flush=True)
            break
        except Exception as e: 
            print(f"ERR: Critical -> {e}", flush=True)
            time.sleep(2)

if __name__ == "__main__":
    main()
