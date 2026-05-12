import re
import math
import time
from pathlib import Path
import config

class Character:
    def __init__(self, file_path):
        self.path = Path(file_path)
        self.name = "Unknown"
        self.base_level = 1
        self.base_exp = 0
        self.base_stats = {}
        
        self.level = 1
        self.exp = 0
        self.exp_needed = 100
        self.stats = {}
        
        self.load_and_process()

    def load_and_process(self):
        try:
            self.content = self.path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"ERROR: Failed to read {self.path.name} -> {e}", flush=True)
            return

        # Split content into parts to protect the Base section
        parts = self.content.split(config.STATUS_HEADER)
        self.base_section = parts[0]
        self.status_section = parts[1] if len(parts) > 1 else ""

        # 1. Parse Name
        name_match = re.search(r"# Name:\s*(.*)", self.base_section)
        if name_match: self.name = name_match.group(1).strip()

        # 2. Parse Base State
        b_lvl_match = re.search(r"(?:Base\s+)?Level:\s*(\d+)", self.base_section, re.IGNORECASE)
        b_exp_match = re.search(r"(?:Base\s+)?EXP:\s*(\d+)", self.base_section, re.IGNORECASE)
        
        self.base_level = int(b_lvl_match.group(1)) if b_lvl_match else 1
        self.base_exp = int(b_exp_match.group(1)) if b_exp_match else 0
        self.base_stats = {m.group(1).upper(): int(m.group(2)) for m in re.finditer(config.STAT_PATTERN, self.base_section)}

        self.level = self.base_level
        self.exp = self.base_exp
        self.exp_needed = self.level ** 2 * 100
        self.stats = self.base_stats.copy()

        # 3. Process Log
        log_section_match = re.search(r"## Log\s*\n(.*?)(?=\n##|$)", self.base_section, re.DOTALL)
        if log_section_match:
            actions = log_section_match.group(1).strip().split('\n')
            for action in actions:
                action = action.strip()
                if not action: continue

                s_match = re.search(r"([A-Z]{2,3})\s*([+-]\d+)", action)
                if s_match:
                    stat_name = s_match.group(1).upper()
                    if stat_name in self.stats:
                        self.stats[stat_name] += int(s_match.group(2))
                    continue

                kill_words = "|".join(config.KEYWORDS["KILL"])
                gain_words = "|".join(config.KEYWORDS["GAIN"])
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
                        except ValueError: pass

    def save(self):
        """Reconstructs the file with the updated status block at the end."""
        display_stats = {k: v for k, v in self.stats.items() if k not in ["LEVEL", "EXP"]}
        stats_str = " | ".join([f"{k}: {v}" for k, v in display_stats.items()])
        
        status_content = f"{config.STATUS_HEADER}\n"
        status_content += f"Level: {self.level}\n"
        status_content += f"EXP: {self.exp}/{self.exp_needed}\n"
        status_content += f"{stats_str}\n"

        # Re-attach the status block to the protected base section
        new_content = self.base_section.rstrip() + "\n\n" + status_content

        if new_content != self.content:
            try:
                self.path.write_text(new_content, encoding='utf-8')
                self.content = new_content
                return True
            except Exception as e:
                print(f"ERR: Save failed {self.path.name} -> {e}", flush=True)
        return False

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
        
        total_gained = 0
        print(f"\nCALC: {self.name} vs {monster_name} (x{qty})", flush=True)
        print(f"  Base Reward: {m_reward} EXP", flush=True)

        for i in range(1, qty + 1):
            # Dynamic multiplier: Recalculated for EVERY individual kill
            gap = m_lvl - self.level
            multiplier = max(0, 1 + (gap * 0.2))
            gained = math.floor(m_reward * multiplier)
            
            old_lvl = self.level
            self.exp += gained
            total_gained += gained
            self._check_level_up()
            
            # Print if multiplier changes or level up happens
            if i == 1:
                print(f"  Start Gap: {gap} | Multiplier: {multiplier:.2f}x", flush=True)
            
            if self.level > old_lvl:
                print(f"  > Kill #{i}: LEVEL UP to {self.level} (Gap now {m_lvl - self.level})", flush=True)
            
            if multiplier <= 0 and gained == 0:
                print(f"  > Kill #{i}: Gap too large ({gap}). EXP gain halted.", flush=True)
                break
        
        print(f"  RESULT: +{total_gained} Total EXP Gained\n", flush=True)

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
                        print(f"UPDATED: {char.name} (Result: Lv {char.level})", flush=True)
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
