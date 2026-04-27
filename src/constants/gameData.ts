export const STATS = ["STR", "VIT", "AGI", "DEX", "MNA"] as const;
export type StatType = typeof STATS[number];

export const ROLE_PRESETS: Record<string, Record<StatType, number>> = {
  adventurer: { STR: 6, AGI: 6, VIT: 4, DEX: 4, MNA: 3 },
  paladin: { STR: 7, VIT: 8, AGI: 3, DEX: 3, MNA: 2 },
  merchant: { STR: 3, VIT: 4, AGI: 3, DEX: 4, MNA: 2 },
  scholar: { STR: 2, VIT: 3, AGI: 2, DEX: 3, MNA: 8 },
  rogue: { STR: 4, VIT: 3, AGI: 9, DEX: 7, MNA: 2 },
  soldier: { STR: 8, VIT: 7, AGI: 4, DEX: 3, MNA: 1 },
  ranger: { STR: 5, VIT: 4, AGI: 7, DEX: 8, MNA: 2 },
  mage: { STR: 2, VIT: 3, AGI: 3, DEX: 3, MNA: 10 },
};

export const KEYWORD_STAT_BONUSES: Record<string, { stat: StatType; bonus: number }> = {
  swordsman: { stat: "STR", bonus: 12 },
  marathon: { stat: "VIT", bonus: 10 },
  archer: { stat: "DEX", bonus: 10 },
  mage: { stat: "MNA", bonus: 12 },
  wizard: { stat: "MNA", bonus: 14 },
  blacksmith: { stat: "STR", bonus: 8 },
  "one-man-army": { stat: "STR", bonus: 14 },
  paladin: { stat: "VIT", bonus: 8 },
  adventurer: { stat: "AGI", bonus: 4 },
};

export const MP_GROWTH_RATE = 0.048; // 4.8%

export const AGE_BASELINES = [
  { maxAge: 17, stats: { STR: 5, VIT: 5, AGI: 6, DEX: 5, MNA: 4 } },
  { maxAge: 29, stats: { STR: 8, VIT: 8, AGI: 8, DEX: 8, MNA: 6 } },
  { maxAge: 44, stats: { STR: 9, VIT: 10, AGI: 7, DEX: 8, MNA: 8 } },
  { maxAge: 150, stats: { STR: 7, VIT: 9, AGI: 6, DEX: 7, MNA: 7 } },
];
