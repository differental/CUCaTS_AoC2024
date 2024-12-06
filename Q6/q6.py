
import png # https://pypng.readthedocs.io/en/latest/
import os

SHARD_WIDTH = 112
SHARD_HEIGHT = 64

X_SHARDS = 16
Y_SHARDS = 16

class Shard:
    def __init__(self, width, height, pixels, filename):
        self.width = width
        self.height = height
        self.pixels = pixels
        self.filename = filename
    
    def build_edges(self):
        pass
    
    def compare_to_opposite_edge(self, edge_no, other):
        pass


def main():
    files = os.listdir("chunks")
    for filename in files:
        reader = png.Reader(filename=f"chunks/{filename}")
        width, height, pixels, metadata = reader.read()
        shard = Shard(width, height, pixels, filename)
    
    # TODO:
    # - calculate 4 * n^2 shard connection scores, for every pair of shards and every edge
    # - match shards together greedily with highest scores
    # - output the stitched image


if __name__ == "__main__":
    main()


