import math

# Base mana for MP1
base_mp = float(input("Enter the base mp: "))
mp_total = base_mp

# Ask user for the fixed growth rate (same for all MPs)
growth_rate = float(4.8) / 100

# Store results as (MP#, total mana, increase, formula string)
mana_list = [(1, mp_total, 0.0, f"MP1 = {base_mp}")]

# Calculate mana for MP2 to MP100
for k in range(2, 501):
    previous_total = mp_total
    mp_total = previous_total + previous_total * growth_rate

    # Floor the total for display
    floored_total = math.floor(mp_total)
    floored_previous = math.floor(previous_total)

    # Calculate increase based on floored totals
    increase = floored_total - floored_previous

    formula = f"[{previous_total:.6f} + ({previous_total:.6f} x {growth_rate*100:.2f}%)]"
    mana_list.append((k, floored_total, increase, formula))

# Print results
for mp_num, mana, increase, formula in mana_list:
    print(f"MP{mp_num} = {mana} mana, increase = {increase}, calculation: {formula}")


