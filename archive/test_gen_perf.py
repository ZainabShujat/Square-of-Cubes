import sys
sys.path.insert(0, '.')

import time
from core.levels import generate_inventory, get_max_tile

# Test a sample of board sizes
test_sizes = [4, 6, 8, 9, 10, 12, 14, 15, 16]

print("Testing generate_inventory for sample board sizes...")
print(f"{'Board':>6} {'MaxTile':>8} {'Time(s)':>10} {'Inventory Summary':50}")
print("-" * 80)

total_time = 0
for board_size in test_sizes:
    start = time.time()
    result = generate_inventory(board_size)
    elapsed = time.time() - start
    total_time += elapsed
    
    max_tile = get_max_tile(board_size)
    inv = result['inventory']
    inv_str = ', '.join(f"{k}x{v}" for k, v in sorted(inv.items(), reverse=True))
    
    print(f"{board_size:6} {max_tile:8} {elapsed:10.2f}  {inv_str:50}")

print("-" * 80)
print(f"Total time for {len(test_sizes)} levels: {total_time:.2f}s")
print(f"Average time per level: {total_time / len(test_sizes):.2f}s")
