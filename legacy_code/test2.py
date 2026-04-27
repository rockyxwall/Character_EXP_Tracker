import math

# Base energy for ENP1
base_enp = float(input("Enter the base ENP: "))
growth_rate = 50  # percent
enp_total = base_enp

# Store results as (ENP#, total, increase, formula)
energy_list = [(1, enp_total, 0.0, f"ENP1 = {base_enp}")]

# Calculate ENP2 to ENP100
for k in range(2, 101):
    # Decrease growth rate by 0.4% every 10 ENPs (after each full set)
    if (k - 1) % 10 == 0:
        growth_rate -= 1

    previous_total = enp_total
    enp_total = previous_total + previous_total * (growth_rate / 100)

    increase = enp_total - previous_total
    floored_total = math.floor(enp_total)

    formula = f"[{previous_total:.6f} + ({previous_total:.6f} x {growth_rate:.2f}%)]"
    energy_list.append((k, floored_total, increase, formula))

# Print results
for enp_num, total, increase, formula in energy_list:
    print(f"ENP{enp_num}: {total} (raw: {total + (increase - math.floor(increase)):.6f}), "
          f"increase: {increase:.6f}, calc: {formula}")


