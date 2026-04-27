import math


def round_half_down(x):
    frac = x - math.floor(x)
    return math.ceil(x) if frac > 0.5 else math.floor(x)


# Parameters
base_enp = float(input("Enter base ENP: "))
growth_percent = 20.0  # starting percent
decrease_every = 10    # decrease growth after every this many ENPs
decrease_amount = 0.4  # percent to subtract each step
max_enp = 100

# State
raw_total = base_enp
rounded_total = round_half_down(raw_total)

results = [(1, rounded_total, raw_total, 0.0,
            f"ENP1 = {rounded_total} (raw {raw_total:.6f})")]

for k in range(2, max_enp + 1):
    # decrease growth before computing ENP(k) when entering next decade (ENP11, ENP21, ...)
    if (k - 1) % decrease_every == 0:
        growth_percent = max(0.0, growth_percent - decrease_amount)

    prev_rounded = rounded_total

    # formula uses the rounded previous value
    raw_total = prev_rounded + prev_rounded * (growth_percent / 100.0)
    rounded_total = round_half_down(raw_total)

    increase_rounded = rounded_total - prev_rounded
    increase_raw = raw_total - prev_rounded

    formula = f"[{prev_rounded} + ({prev_rounded} x {growth_percent:.2f}%)]"

    results.append((k, rounded_total, raw_total, increase_rounded, formula))

# Print results
for enp_num, r_total, raw, inc_r, formula in results:
    print(f"ENP{enp_num}: rounded = {r_total}, raw = {raw:.6f}, "
          f"rounded_increase = {inc_r}, calc = {formula}")


