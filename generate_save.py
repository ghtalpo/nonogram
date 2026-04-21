rows = 30
cols = 30
chints = """
2 4 2 2
9 1 3 4
11 6
2 11 2 3 3
1 9 4 4
3 6 4 5
2 3 3 5
2 2 5
3 2 4 3
6 1 3 1
1 4 2 3
4 1 2
1 6 4
9 5
1 11 12
2 1 8 5
2 7 1 4
2 4 2 3 2
2 2 1 3 1
1 4 2 3 3
6 2 6
8 3 6
1 4 3 6
3 6 2 5
3 6 1 3 4
4 3 4 3
3 4 6
1 1 2 2 4
1 1 4 2 2 3
2 4 1
"""
rhints = """
2 2 2 2
1 2 1 4 1 1
1 1 2 2 4 1
1 2 6
4 1 1 1 3
4 2 2 1 3
6 1 2 1 2 2
7 3 6 3 1 1
11 11 1
25 2
5 8 9
5 6 7
1 1 12 4
1 1 2 1 4 1 2 1 1
1 2 6 2 1
1 1 1 1
1 2 2 1 2
1 1 1 1
1 1 1 1 1 2 1
1 2 1 1 1 2 1
2 1 2 1 2 1
1 1 1 1 1 2 1
2 2 1 2 1 1
1 1 1 1 1
2 1 1 4 2
1 4 3 4 1
2 4 5 5 2
8 5 10
9 7 10
10 19
"""
output = "nono.json"

chints = [[int(x) for x in x.split()] for x in chints.split('\n') if x]
assert(len(chints) == cols)
print('len(chints)? %d == cols? %d' % (len(chints), cols))

rhints = [[int(x) for x in x.split()] for x in rhints.split('\n') if x]
assert(len(rhints) == rows)
print('len(rhints)? %d == rows? %d' % (len(rhints), rows))

def check_trivials(chints, rhints, cols, rows):
    for i in range(len(chints)):
        hint = chints[i]#[int(x) for x in chints[i].get().split()]
        s = sum(hint) + len(hint)-1
        rem = rows - s
        assert rem >= 0, "wrong chints at line no: %d" % (i+1)

    for i in range(len(rhints)):
        hint = rhints[i]# = [int(x) for x in rhints[i].get().split()]
        s = sum(hint) + len(hint)-1
        rem = cols - s
        assert rem >= 0, "wrong rhints at line no: %d" % (i+1)

check_trivials(chints, rhints, cols, rows)

cheight = max([len(x) for x in chints])
import json
ch = [' '.join([str(x) for x in l]) for l in chints]
rh = [' '.join([str(x) for x in l]) for l in rhints]
encoded = json.dumps({'rows':rows, 'cols':cols, 'chints': ch, 'rhints': rh, 'map': [[" "]], 'cheight': cheight})
encoded += '\n'
with open('nono.json', 'w') as f:
    f.writelines(encoded)
    f.close()

print('done')