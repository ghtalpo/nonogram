from data import cols, rows, chints, rhints

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
