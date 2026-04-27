import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { AGE_BASELINES, ROLE_PRESETS, KEYWORD_STAT_BONUSES, STATS, StatType } from "../constants/gameData";
import { calcExpToNext, calcThreshold, calcMonsterBaseExp, calcExpGainMultiplier } from "../logic/formulas";

interface CharacterState {
  name: string;
  race: string;
  level: number;
  currentExp: number;
  expToNext: number;
  stats: Record<StatType, number>;
  baseMp: number;
  skills: string[];
  titles: string[];
  gift: string;
  isCreated: boolean;

  // Actions
  setName: (name: string) => void;
  createCharacter: (age: number | null, role: string | null, keywords: string[]) => void;
  gainExp: (monsterLevel: number, quantity: number) => void;
  reset: () => void;
}

const getInitialStats = (): Record<StatType, number> => {
  const s = {} as Record<StatType, number>;
  STATS.forEach((stat) => (s[stat] = 0));
  return s;
};

export const useCharacterStore = create<CharacterState>()(
  persist(
    (set, get) => ({
      name: "Unknown",
      race: "Human",
      level: 1,
      currentExp: 0,
      expToNext: calcExpToNext(1),
      stats: getInitialStats(),
      baseMp: 10,
      skills: [],
      titles: [],
      gift: "",
      isCreated: false,

      setName: (name) => set({ name }),

      createCharacter: (age, role, keywords) => {
        const stats = getInitialStats();
        
        // Age baseline
        const baseline = AGE_BASELINES.find(b => age === null || age <= b.maxAge)?.stats || AGE_BASELINES[AGE_BASELINES.length-1].stats;
        STATS.forEach(s => stats[s] += baseline[s]);

        // Role
        if (role) {
          const preset = ROLE_PRESETS[role.toLowerCase()];
          if (preset) {
            STATS.forEach(s => {
              const rnd = Math.floor(Math.random() * 6) - 2; // -2 to 3
              stats[s] += Math.max(0, preset[s] + rnd);
            });
          }
        }

        // Keywords
        keywords.forEach(kw => {
          const bonus = KEYWORD_STAT_BONUSES[kw.toLowerCase()];
          if (bonus) {
            stats[bonus.stat] += bonus.bonus;
          }
        });

        // Small random bonus
        STATS.forEach(s => stats[s] += Math.floor(Math.random() * 4));

        set({ 
          stats, 
          isCreated: true, 
          level: 1, 
          currentExp: 0, 
          expToNext: calcExpToNext(1) 
        });
      },

      gainExp: (monsterLevel, quantity) => {
        let { currentExp, level, stats, expToNext } = get();
        const baseExpPerKill = calcMonsterBaseExp(monsterLevel);

        for (let i = 0; i < quantity; i++) {
          // Level 1 gate
          if (level === 1 && !STATS.some(s => stats[s] >= 5)) break;

          const mult = calcExpGainMultiplier(monsterLevel, level);
          const gained = Math.floor(baseExpPerKill * mult);
          currentExp += gained;

          while (currentExp >= expToNext) {
            currentExp -= expToNext;
            level += 1;
            expToNext = calcExpToNext(level);

            // Stat bump logic
            const threshold = calcThreshold(level);
            const topStat = (Object.entries(stats) as [StatType, number][]).reduce((a, b) => a[1] > b[1] ? a : b)[0];
            if (stats[topStat] < threshold) {
              stats[topStat] = threshold;
            }
          }
        }

        set({ currentExp, level, stats, expToNext });
      },

      reset: () => set({
        name: "Unknown",
        race: "Human",
        level: 1,
        currentExp: 0,
        expToNext: calcExpToNext(1),
        stats: getInitialStats(),
        baseMp: 10,
        skills: [],
        titles: [],
        gift: "",
        isCreated: false,
      }),
    }),
    {
      name: "character-storage",
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
