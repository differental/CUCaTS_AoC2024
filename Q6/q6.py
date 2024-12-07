import png # https://pypng.readthedocs.io/en/latest/
import os
import numpy as np
import math

SHARD_WIDTH = 112 * 3
SHARD_HEIGHT = 64

X_SHARDS = 16
Y_SHARDS = 16

class Shard:
    def __init__(self, width, height, pixels, filename):
        self.width = width
        self.height = height
        self.pixels = np.vstack([np.uint8(row) for row in pixels])
        self.filename = filename
        
    def build_edges(self):
        self.edges = [
            self.pixels[:, :3], # left
            self.pixels[0, :].reshape(-1, 3), # top 
            self.pixels[:, -3:], # right 
            self.pixels[-1, :].reshape(-1, 3) # bottom
        ]
    
    def compare_to_opposite_edge(self, edge_no, other):
        other_edge_no = (edge_no + 2) % 4

        edge_a = self.edges[edge_no]
        edge_b = other.edges[other_edge_no]
        
        diff = np.abs(edge_a - edge_b)
        
        diff_squared = np.square(edge_a - edge_b)
        
        return np.sum(diff_squared) / diff_squared.size

def main():
    files = os.listdir("chunks")
    shards = []

    grid = np.full((16, 16), None)
    locations = {}

    for filename in files:
        reader = png.Reader(filename=f"chunks/{filename}")
        width, height, pixels, metadata = reader.read()
        shard = Shard(width, height, pixels, filename)
        shard.build_edges()
        shards.append(shard)

        if shard.filename == "chunk_964560701.png":
            grid[15][15] = shard 
            locations[shard] = (15, 15)

    scores = []

    for i in range(len(shards) - 1):
        for j in range(i+1, len(shards)):
            
            shard_a = shards[i]
            shard_b = shards[j]

            for direction in range(4):
                scores.append((shard_a, shard_b, direction, shard_a.compare_to_opposite_edge(direction, shard_b)))

    scores = sorted(scores, key=lambda x: x[3])
    
    # directions of the second image relative to the first
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    while len(locations.keys()) < 256:
        for score in scores:
            shard_a, shard_b, direction, val = score
            
            if shard_a in locations.keys() and shard_b in locations.keys():
                continue

            if shard_a not in locations.keys() and shard_b not in locations.keys():
                continue 

            if shard_a in locations.keys():
                dx, dy = directions[direction]
                x, y = locations[shard_a]
                
                if x+dx<0 or x+dx>15 or y+dy<0 or y+dy>15:
                    continue

                if grid[x+dx][y+dy]:
                    continue

                grid[x+dx][y+dy] = shard_b 
                locations[shard_b] = (x+dx, y+dy)
                
                break

            if shard_b in locations.keys():
                dx, dy = directions[direction]
                x, y = locations[shard_b]

                if x-dx<0 or x-dx>15 or y-dy<0 or y-dy>15:
                    continue
                
                if grid[x-dx][y-dy]:
                    continue

                grid[x-dx][y-dy] = shard_a 
                locations[shard_a] = (x-dx, y-dy)

                break
            
    final_image = np.zeros((Y_SHARDS * SHARD_HEIGHT, X_SHARDS * SHARD_WIDTH), dtype=np.uint8)
    for y in range(Y_SHARDS):
        for x in range(X_SHARDS):
            shard = grid[x][y]
            final_image[y * SHARD_HEIGHT:(y + 1) * SHARD_HEIGHT,
                        x * SHARD_WIDTH:(x + 1) * SHARD_WIDTH] = shard.pixels

    image = png.from_array(final_image, "RGB")
    image.save("output.png")

if __name__ == "__main__":
    main()
