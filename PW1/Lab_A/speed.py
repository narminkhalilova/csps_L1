# compare speed of the loop version and the numpy version of the simulation
import time
from decay import simulate, simulate_loop

n0 = 200000   # number of atoms
steps = 10    # number of time steps, kept small so the loop finishes

# time the pure python loop version
start = time.perf_counter()
simulate_loop(n0, 0.3, steps=steps)
t_loop = time.perf_counter() - start

# time the numpy version
start = time.perf_counter()
simulate(n0, 0.3, steps=steps)
t_numpy = time.perf_counter() - start

print(f"loop    : {t_loop:.6f} s")
print(f"numpy   : {t_numpy:.6f} s")
print(f"speed-up: {t_loop / t_numpy:.2f} x faster")
