import time
import heapq

# Gets valid successors for the current state
def get_successors(player, crates, walls):
        successors = []
        directions = {'u': (0, -1), 'd': (0, 1), 'l': (-1, 0), 'r': (1, 0)}

        for action, (dx, dy) in directions.items():
            next_player = (player[0] + dx, player[1] + dy)

            if next_player in walls:
                continue  # Can't move into a wall

            if next_player in crates:
                next_crate = (next_player[0] + dx, next_player[1] + dy)

                if next_crate in walls or next_crate in crates:
                    continue  # Can't push crate into a wall or another crate

                new_crates = list(crates)
                new_crates.remove(next_player)
                new_crates.append(next_crate)
                successors.append((next_player, tuple(sorted(new_crates)), action))
            else:
                # Player steps onto empty floor or target
                successors.append((next_player, crates, action))

        return successors

# Clearly now we get successors for the current state, but we also need to check if the new state is valid (i.e., not a deadlock). For now, let's assume all successors are valid.
def is_corner_deadlock(crate_pos, walls, goals):
    #True if corner deadlock, false if not
    x, y = crate_pos

    if crate_pos in goals:
        return False  # Not a deadlock if the crate is on a goal

    # Checking for adjacent walls to determine if the crate is in a corner
    wall_up = (x, y - 1) in walls
    wall_down = (x, y + 1) in walls
    wall_left = (x - 1, y) in walls
    wall_right = (x + 1, y) in walls

    # Checks 90 degree possibilities
    if (wall_up and wall_left) or (wall_up and wall_right) or (wall_down and wall_left) or (wall_down and wall_right):
        return True  # Crate is in a corner deadlock

    return False  # Crate is not in a corner deadlock


#A* stuff aka the main stuff aka i wanna die
class SokoBot:
    def solveSokobanPuzzle(self, width, height, mapData, itemsData):
        walls = set()
        goals = set()
        player_pos = None
        crates = []

        for y in range(height):
            for x in range(width):
                # Check static map tiles
                if mapData[y][x] == '#':
                    walls.add((x, y))
                elif mapData[y][x] == '.':
                    goals.add((x, y))

                # Check dynamic item tiles
                if itemsData[y][x] == '@':
                    player_pos = (x, y)
                elif itemsData[y][x] == '$':
                    crates.append((x, y))

        # Convert the crate list into a sorted, hashable tuple
        crates_start = tuple(sorted(crates))

        # Verification prints (remove later)
        print(f"Walls count: {len(walls)}, Goals count: {len(goals)}")
        print(f"Player start: {player_pos}")
        print(f"Crates start: {crates_start}")