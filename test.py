a = ['abc123', 'bgf54']


def index(a, txt):
    for idx, val in enumerate(a):
        if txt in val:
            return idx
    return False


x = index(a, "abc")
if type(x) is int:
    print(x)
else:
    print("Folder not found")
