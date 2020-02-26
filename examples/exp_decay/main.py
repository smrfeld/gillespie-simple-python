from gillespie_simple import *

from pathlib import Path

# Reaction
rxn = Rxn("test",3.0,["A"],[])

# Initial counts
counts = Counts()
counts.set_count("A",100)

# Run
counts_hist = run_gillespie(
    rxn_list=[rxn],
    counts=counts,
    dt_st_every=0.1,
    t_max=100
    )

# Print
print(counts_hist.get_count_hist("A"))

# Write
Path("data").mkdir(parents=True, exist_ok=True)
counts_hist.write_count_hist("A", "data/A.txt")
