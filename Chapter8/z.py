def kw(**kwargs):
    print(type(kwargs), kwargs)


kw(**{"a":100, "b":200})
kw(a=100, b=200)