from core.solver import level_is_solvable
from core.levels import LEARNING_LEVELS

print('solver 4 full tile:', level_is_solvable(4, {4:1}))
print('solver 4 small inv (3+1):', level_is_solvable(4, {3:1,1:1}))
for l in LEARNING_LEVELS[:3]:
    solvable = level_is_solvable(l.board_size, l.inventory, max_nodes=60000)
    print('level', l.number, l.board_size, 'solvable?', solvable, 'summary:', l.inventory)
