import os

# Parameters
base_mana = 5.0
soft_cap = 5000.0        # maximum mana
max_enp = 1000
growth_rate = 1.0        # % of remaining gap per ENP for smooth progression

# Standard rounding


def round_standard(x):
    return int(x + 0.5)


# Prepare unique filename
base_filename = "ENP_progression.txt"
filename = base_filename
counter = 1
while os.path.exists(filename):
    filename = f"ENP_progression_{counter}.txt"
    counter += 1

# Initial state
raw_mana = base_mana
results = [(1, round_standard(raw_mana), raw_mana, 0.0,
            f"ENP1 = {round_standard(raw_mana)} (raw {raw_mana:.6f})")]

# Calculate ENPs
for enp in range(2, max_enp + 1):
    prev_raw = raw_mana
    # Diminishing returns formula (smooth early progression)
    raw_mana = prev_raw + (soft_cap - prev_raw) * (growth_rate / 100.0)
    rounded_mana = round_standard(raw_mana)
    rounded_increase = round_standard(raw_mana - prev_raw)

    formula = f"[{prev_raw:.6f} + ({soft_cap:.6f} - {prev_raw:.6f}) x {growth_rate:.2f}%]"
    results.append((enp, rounded_mana, raw_mana, rounded_increase, formula))

# Write to file
with open(filename, "w") as f:
    for enp_num, r_mana, raw, inc_r, formula in results:
        f.write(f"ENP{enp_num}: rounded = {r_mana}, raw = {raw:.6f}, "
                f"rounded_increase = {inc_r}, calc = {formula}\n")

print(f"Progression for {max_enp} ENPs saved to {filename}")


