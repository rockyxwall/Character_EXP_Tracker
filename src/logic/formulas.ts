import { MP_GROWTH_RATE, StatType } from "../constants/gameData";

export const calcExpToNext = (level: number) => level ** 2 * 10;

export const calcThreshold = (level: number) => level * 5;

export const calcMonsterBaseExp = (monsterLevel: number) => 
  Math.floor((monsterLevel ** 2 * 10) * 0.1);

export const calcExpGainMultiplier = (monsterLevel: number, playerLevel: number) => {
  const diff = monsterLevel - playerLevel;
  const mult = 1.0 + 0.2 * diff;
  return mult > 0 ? mult : 0.0;
};

export const calcMPGrowth = (baseMp: number, mna: number) => {
  let mpTotal = baseMp;
  const rows: { mpLevel: number; total: number; increase: number; formula: string }[] = [
    { mpLevel: 1, total: Math.floor(mpTotal), increase: 0, formula: `MP1 = ${baseMp}` }
  ];

  for (let k = 2; k <= mna; k++) {
    const prev = mpTotal;
    mpTotal = prev + prev * MP_GROWTH_RATE;
    const flooredTotal = Math.floor(mpTotal);
    const flooredPrev = Math.floor(prev);
    const increase = flooredTotal - flooredPrev;
    const formula = `[${prev.toFixed(6)} + (${prev.toFixed(6)} x ${(MP_GROWTH_RATE * 100).toFixed(2)}%)]`;
    rows.push({ mpLevel: k, total: flooredTotal, increase, formula });
  }

  return { rows, total: Math.floor(mpTotal) };
};
