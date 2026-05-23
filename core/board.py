from utils.constants import BOARD_SIZE


class Board:

    def __init__(self):

        self.size = BOARD_SIZE

    # =====================================================
    # CELL OCCUPANCY
    # =====================================================

    def get_occupied_cells(self, state):

        occupied = set()

        for piece in state.placed_pieces:

            if piece.grid_x is None or piece.grid_y is None:
                continue

            for y in range(piece.grid_y, piece.grid_y + piece.size):

                for x in range(piece.grid_x, piece.grid_x + piece.size):

                    occupied.add((x, y))

        return occupied

    def is_cell_filled(self, state, x, y):

        return (x, y) in self.get_occupied_cells(state)

    # =====================================================
    # PLACEMENT VALIDATION
    # =====================================================

    def can_place(self, state, size, grid_x, grid_y):

        # outside board
        if grid_x < 0 or grid_y < 0:
            return False

        if grid_x + size > self.size:
            return False

        if grid_y + size > self.size:
            return False

        occupied = self.get_occupied_cells(state)

        # overlap check
        for y in range(grid_y, grid_y + size):

            for x in range(grid_x, grid_x + size):

                if (x, y) in occupied:
                    return False

        return True

    # =====================================================
    # EMPTY CELLS
    # =====================================================

    def get_empty_cells(self, state):

        empty = []
        occupied = self.get_occupied_cells(state)

        for y in range(self.size):

            for x in range(self.size):

                if (x, y) not in occupied:

                    empty.append((x, y))

        return empty

    # =====================================================
    # FLOOD FILL REGIONS
    # =====================================================

    def get_regions(self, state):

        empty = set(self.get_empty_cells(state))

        visited = set()

        regions = []

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        for cell in empty:

            if cell in visited:
                continue

            stack = [cell]

            region = []

            while stack:

                current = stack.pop()

                if current in visited:
                    continue

                visited.add(current)

                region.append(current)

                cx, cy = current

                for dx, dy in directions:

                    nx = cx + dx
                    ny = cy + dy

                    neighbor = (nx, ny)

                    if neighbor in empty and neighbor not in visited:

                        stack.append(neighbor)

            regions.append(region)

        return regions

    # =====================================================
    # DEAD REGIONS
    # =====================================================

    def get_dead_regions(self, state):

        remaining_areas = []

        for size, count in state.remaining_tiles.items():

            remaining_areas.extend(
                [size * size] * count
            )

        dead = []

        regions = self.get_regions(state)

        for region in regions:

            region_area = len(region)

            possible = False

            # exact square possible
            for area in remaining_areas:

                if region_area % area == 0:
                    possible = True
                    break

            if not possible:
                dead.append(region)

        return dead