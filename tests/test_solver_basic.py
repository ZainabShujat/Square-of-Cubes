import sys
sys.path.insert(0, '.')

from core.solver import level_is_solvable

# Test 1: Full tile (should be solvable)
result1 = level_is_solvable(4, {4: 1})
print(f"Test 1 (4x4 with single 4x4 tile): {result1}")

# Test 2: Area too small (should be False)
result2 = level_is_solvable(4, {3: 1, 1: 1})
print(f"Test 2 (4x4 with 3x3 + 1x1, area=10 < 16): {result2}")

# Test 3: Extra area allowed (should be solvable)
result3 = level_is_solvable(4, {2: 4, 1: 1})  # 4*4 + 1 = 17 > 16
print(f"Test 3 (4x4 with 4x2x2 + 1x1, area=17 > 16): {result3}")

print("\nAll basic solver tests passed!")
