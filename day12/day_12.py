import os

filename="input_12.txt"
filepath="/home/G5636/Téléchargements"

file_to_read = os.path.join(filepath,filename)

with open(file_to_read) as f:
    *shapes, regions = f.read().strip().split("\n\n")

sizes = [sum(c == "#" for c in shape) for shape in shapes]

part1 = 0
for region in regions.split("\n"):
    w, h, *nums = map(int, region.replace("x", " ").replace(":", "").split(" "))
    if w * h >= sum(n * size for n, size in zip(nums, sizes)):
        part1 += 1

print(part1)