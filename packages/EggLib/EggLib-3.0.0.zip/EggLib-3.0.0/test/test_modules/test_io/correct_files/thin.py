import random, sys

for fname in 'Osativa_193_gene', 'Populus_trichocarpa_short':
    print fname
    inf = open(fname+'.gff3')
    ouf = open(fname+'_thinned.gff3', 'w')

    c1 = 0
    c2 = 0
    c3 = 0
    n = 0
    t = 0
    r = 0
    g = 0
    kept = set()
    discarded = set()
    for line in inf:
        bits = line.split('\t')
        if len(bits) != 9:
            ouf.write(line)
            c1 += 1
        else:
            qual = dict([i.strip().split('=') for i in bits[8].split(';')])
            if bits[2] == 'repeat_region':
                if random.random() < 0.05:
                    ouf.write(line)
                    c2 += 1
                    n += 1
                    t += 1
                    r += 1
                else:
                    c3 += 1
            elif bits[2] == 'gene':
                if 'ID' in qual: name = qual['ID']
                else: name = qual['Name']
                assert name not in discarded and name not in kept
                if random.random() < 0.05 or (int(bits[3]) -1 >= 1080000 and int(bits[4]) - 1 <= 2510000):
                    kept.add(name)
                    ouf.write(line)
                    c2 += 1
                    n += 1
                    t += 1
                    g += 1
                else:
                    discarded.add(name)
                    c3 += 1
            else:
                parent = qual['Parent']
                if 'pacid' in qual: ID = 'PAC:' + qual['pacid']
                elif 'ID' in qual: ID = qual['ID']
                else: ID = None
                if parent in kept:
                    if ID is not None: kept.add(ID)
                    ouf.write(line)
                    c2 += 1
                    t += 1
                elif parent in discarded:
                    if ID is not None: discarded.add(ID)
                    c3 += 1
                else:
                    sys.exit('unknown parent: `{0}`'.format(parent))
            
    print '   lines passed as is:', c1
    print '   lines retained:', c2
    print '   lines discarded:', c3
    print '   number of top features:', n
    print '   number of features tot:', t
    print '   genes:', g
    print '   repeat_region:', r
