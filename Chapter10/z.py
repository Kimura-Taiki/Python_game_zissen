def b(b):
    print("bool")
    return b

print([print("True") for _ in range(5) if b(True)])
# [print("True") if b(True) else print("False") for _ in range(5)]
# [print("True") if b(False) else print("False")]