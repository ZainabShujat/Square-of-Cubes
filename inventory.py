import csv

AREA = 14 * 14

rows = []

for n4 in range(1, AREA // 16 + 1):
    rem4 = AREA - 16 * n4

    for n3 in range(1, rem4 // 9 + 1):
        rem3 = rem4 - 9 * n3

        for n2 in range(1, rem3 // 4 + 1):

            n1 = rem3 - 4 * n2

            if n1 < 0:
                continue

            if n1 > 10:
                continue

            total_tiles = n1 + n2 + n3 + n4

            rows.append([
                n1,
                n2,
                n3,
                n4,
                total_tiles
            ])

rows.sort(key=lambda r: r[4])

with open("14x14_candidates.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "1x1",
        "2x2",
        "3x3",
        "4x4",
        "TotalTiles"
    ])

    writer.writerows(rows)

print("Generated", len(rows), "inventories")