a = [[1, 1, 1, 1], [2, 2, 2, 2]]

b = list(a)

for item in b:
    a.append(list(item))

a[0][3] = 5

print(a)