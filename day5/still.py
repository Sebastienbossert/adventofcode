import os

def limitToPreviousRanges(ranges, i, roundUp):
    prev = i
    for range in ranges:
        if range[0] <= i <= range[1]:
            if roundUp:
                i = range[1] + 1
            else:
                i = range[0] - 1
    if i == prev:
        return i
    else:
        return limitToPreviousRanges(ranges, i, roundUp)

file_to_read = os.path.join("/home/G5636/Téléchargements","input_5.txt")
with open(file_to_read, "r", encoding="utf-8") as file:
    inFreshRanges = True
    freshRanges = []
    for line in file:
        line = line.strip()
        if line == '':
            inFreshRanges = False
        elif inFreshRanges:
            freshFrom, freshTo = line.split('-')
            freshFrom, freshTo = int(freshFrom), int(freshTo)
            freshFrom = limitToPreviousRanges(freshRanges, freshFrom, True)
            freshTo = limitToPreviousRanges(freshRanges, freshTo, False)

            if freshFrom > freshTo:
                continue

            for range in freshRanges[:]:
                if (freshFrom <= range[0] <= freshTo) and (freshFrom <= range[1] <= freshTo):
                    freshRanges.remove(range)

            freshRanges.append((freshFrom, freshTo))

    freshCount = 0
    for freshRange in freshRanges:
        freshCount += freshRange[1] - freshRange[0] + 1

    print(freshCount)