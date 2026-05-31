import sys
import os

# ensure project root is on sys.path when running this script from /scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.levels import generate_inventory

for n in (6, 8, 12):
    info = generate_inventory(n)
    print(n, info.get('score'), info.get('tile_count'), info.get('inventory'))
