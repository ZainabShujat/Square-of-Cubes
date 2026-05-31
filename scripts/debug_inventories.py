from core.levels import generate_inventory, get_max_tile

for n in (12,14,16,20,34):
    info = generate_inventory(n)
    print(n, get_max_tile(n), info['inventory'])
