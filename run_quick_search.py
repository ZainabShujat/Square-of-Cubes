from generate_approve_inventories import find_best_for_level
from core.levels import LEARNING_LEVELS

# quick run for levels 2-4
levels_to_run = [2,3,4]
for num in levels_to_run:
    lvl = next((l for l in LEARNING_LEVELS if l.number == num), None)
    if not lvl:
        print(f'Level {num} not found')
        continue
    best, found, elapsed = find_best_for_level(lvl, candidates=100, max_nodes=5000, seed=42)
    print(f'Level {num}: found {found}, elapsed {elapsed:.1f}s')
    if best:
        print('  best:', best)
    else:
        print('  no valid candidate found')
