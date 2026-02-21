import numpy as np 
import random 

class MapGenerator:
    def __init__(self, rowsize=10, columnsize=10, mine_percentage=12):
        self.row = rowsize
        self.column = columnsize
        self.map = np.zeros((self.row, self.column), dtype=int)
        
        # Calculate mines based on a percentage of the total area
        self.total_mines = (self.row * self.column * mine_percentage) // 100
        self.safetiles = (self.row * self.column) - self.total_mines
        self.mine_locations = []

        self._place_mines()
        self._calculate_numbers()

    def _place_mines(self):
        """Guarantees exact mine count using a random sample of coordinates."""
        all_possible_coords = [(r, c) for r in range(self.row) for c in range(self.column)]
        
        # random.sample is perfect here: it picks unique items without replacement
        self.mine_locations = random.sample(all_possible_coords, self.total_mines)
        
        for r, c in self.mine_locations:
            self.map[r][c] = -1

    def _calculate_numbers(self):
        """Iterates through mines and increments neighbors using a vector offset."""
        for r, c in self.mine_locations:
            # Check all 8 neighbors in a 3x3 grid around the mine
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue # Skip the mine itself
                    
                    nr, nc = r + dr, c + dc
                    
                    # Boundary check and ensure we don't overwrite another mine
                    if 0 <= nr < self.row and 0 <= nc < self.column:
                        if self.map[nr][nc] != -1:
                            self.map[nr][nc] += 1

    def __repr__(self):
        return str(self.map)

if __name__ == "__main__":
    # Test with a 10x10 grid
    obj = MapGenerator(10, 10, mine_percentage=15)
    print("Minesweeper Map Matrix:")
    print(obj)