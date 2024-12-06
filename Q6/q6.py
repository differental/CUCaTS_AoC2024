import png # https://pypng.readthedocs.io/en/latest/
import os
import numpy as np

from sklearn.metrics.pairwise import euclidean_distances

SHARD_WIDTH = 336
SHARD_HEIGHT = 64

X_SHARDS = 16
Y_SHARDS = 16

class Shard:
    def __init__(self, width, height, pixels, filename):
        self.width = width
        self.height = height
        self.pixels = np.vstack([np.uint8(row) for row in pixels])
        self.filename = filename

        #print(len(self.pixels), len(self.pixels[0]))
    
    def build_edges(self):
        self.edges = [
            self.pixels[:, 0], # left
            self.pixels[0, :], # top 
            self.pixels[:, -1], # right 
            self.pixels[-1, :] # bottom
        ]
    
    def compare_to_opposite_edge(self, edge_no, other):
        other_edge_no = (edge_no + 2) % 4

        #print(edge_no, other_edge_no)

        edge_a = self.edges[edge_no]
        edge_b = other.edges[other_edge_no]

        #print(euclidean_distances([edge_a], [edge_b])[0][0])
        return euclidean_distances([edge_a], [edge_b])[0][0]

        #print(edge_a, edge_b)
        #print(np.sum(np.abs(edge_a - edge_b)))

        #return np.sum(np.abs(edge_a - edge_b))

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
        
        #print(shard.edges)

    #print(len(shards))
    
    # TODO:
    # - calculate 4 * n^2 shard connection scores, for every pair of shards and every edge
    # - match shards together greedily with highest scores
    # - output the stitched image

    scores = []

    for shard_a in shards:
        for shard_b in shards:
            if shard_a == shard_b:
                continue

            for direction in range(4):
                scores.append((shard_a, shard_b, direction, shard_a.compare_to_opposite_edge(direction, shard_b))) 

    scores = sorted(scores, key=lambda x: x[3])

    #print(scores[0][0].filename, scores[0][1].filename, scores[0][2], int(scores[0][3]))

    #for score in scores:
        #print(score[0].filename, score[1].filename, score[2], int(score[3]))


    # directions of the second image relative to the first
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

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
                
                print(f"{shard_a.filename} placed ({len(locations.keys())}/256)")
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
                
                print(f"{shard_b.filename} placed ({len(locations.keys())}/256)")
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


