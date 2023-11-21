a = [1, 2, 3, 4, 5]
b = [0]*5
for i in range(5):
    b[i] = (b[i-1] if i > 0 else 0)+a[i]

# c = [((_dc := _dc+a[i]) if i > 0 else (_dc := a[i])) for i in range(5)]
temp = 0; c = [(temp := temp+a[i]) for i in range(5)]

print(b)
print(c)
