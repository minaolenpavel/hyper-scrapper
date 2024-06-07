lines = []
with open("./extract.txt", "r") as extract:
    for l in extract:
        lines.append(l)
print(len(lines))