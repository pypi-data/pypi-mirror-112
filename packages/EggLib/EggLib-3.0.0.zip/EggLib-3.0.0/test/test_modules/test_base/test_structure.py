import os, egglib, sys, unittest
from collections import Iterable
import pkg_resources
path = os.path.dirname(__file__)
path_T=os.path.join(path, 'correct_files')
path_F=os.path.join(path, 'erroneous_files')

class Structure_test(unittest.TestCase):
    def test_get_samples(self):
        """ `Structure.get_samples()` """
        d = {
            '1000': { # cluster
                '1100': {    # pop
                    '1110': (0, 1),  # indiv
                    '1120': (2, 3),
                    '1130': (4, 6),
                    '1140': (8, 10)
                },
                '1200': {
                    '1210': (15, 16),
                    '1230': (17, 18),
                    '1240': (19, 20)
                }
            },
            '2000': {
                '2100': {
                    '2110': (21, 22),
                    '2120': (23, 24),
                    '2130': (25, 27),
                    '2140': (26, 28)
                },
                '2200': {
                    '2210': (29, 30),
                    '2220': (31, 32),
                    '2230': (33, 34)
                }
            }
        }
        do = {
            '910': (55, 56),
            '920': (57, 12)
        }

        s = egglib.struct_from_dict(d, do)
        self.assertSetEqual(s.get_samples(),
            set([0,1,2,3,4,6,8,10,15,16,17,18,19,20,21,22,23,24,25,27,26,28,29,30,31,32,33,34]))

    def test_subsetting(self):
        """ subsetting populations using Structure """

        coal = egglib.coalesce.Simulator(4, num_chrom=[5, 2, 5, 4], theta=5.0, migr=0.2)
        cs = egglib.stats.ComputeStats()
        cs.add_stats('nseff', 'S', 'thetaW', 'Pi', 'D', 'FstWC')
        for aln in coal.iter_simul(200):
            sub = aln.subset([5, 6, 12, 13, 14, 15])
            cs.configure(struct=egglib.struct_from_labels(sub, lvl_pop=0))
            ctrl = cs.process_align(sub)
            struct = egglib.struct_from_labels(aln, lvl_pop=0)
            struct = struct.as_dict()[0]
            del struct[None]['0']
            del struct[None]['2']
            struct = egglib.struct_from_dict(struct, None)
            cs.configure(struct=struct)
            test = cs.process_align(aln)
            self.assertDictEqual(ctrl, test)
            if ctrl['S'] > 0:
                self.assertEqual(ctrl['nseff'], 6)

    def test_shuffle(self):
        """ shuffle utility """

        struct = {}
        struct['c1'] = {}
        struct['c1']['p1'] = {}
        struct['c1']['p1']['i1'] = (0, 1)
        struct['c1']['p1']['i2'] = (2, 3)
        struct['c1']['p1']['i3'] = (4, 5)
        struct['c1']['p2'] = {}
        struct['c1']['p2']['i4'] = (6, 7)
        struct['c1']['p2']['i5'] = (8, 9)
        struct['c1']['p2']['i6'] = (10, 11)
        struct['c1']['p2']['i7'] = (12, 13)
        struct['c1']['p3'] = {}
        struct['c1']['p3']['i8'] = (14, 15)
        struct['c1']['p3']['i9'] = (16, 17)
        struct['c1']['p3']['i10'] = (18, 19)
        struct['c2'] = {}
        struct['c2']['p4'] = {}
        struct['c2']['p4']['i11'] = (20, 21)
        struct['c2']['p4']['i12'] = (22, 23)
        struct['c2']['p4']['i13'] = (24, 25)
        struct['c2']['p4']['i14'] = (26, 27)
        struct['c2']['p5'] = {}
        struct['c2']['p5']['i15'] = (28, 29)
        struct['c2']['p5']['i16'] = (30, 31)
        struct['c2']['p5']['i17'] = (32, 33)
        struct['c2']['p5']['i18'] = (34, 35)
        struct = egglib.struct_from_dict(struct, {'i19': (36, 37)})

        def f(x): return int(x[1:])
        def show(s):
            ret = [[],[]]
            ing, otg = struct.as_dict()
            for c in sorted(ing, key=f):
                for p in sorted(ing[c], key=f):
                    for i in sorted(ing[c][p], key=f):
                        ret[0].extend(ing[c][p][i])
            for i in sorted(otg, key=f):
                ret[1].extend(otg[i])
            return ret

        # original structure fingerprint
        original = show(struct)

        # default mode (single shuffling)
        for i in 'it', 'ic', 'is', 'st', 'sc', 'ct':
            n = 0
            for rep in range(20):
                with struct.shuffle(i):
                    ret = show(struct)
                    if ret[0] != original[0]: n += 1
                    self.assertListEqual(ret[1], original[1])
            self.assertGreater(n, 5)
            ret = show(struct)
            self.assertListEqual(ret[0], original[0])
            self.assertListEqual(ret[1], original[1])

        # show that iteration not possible in default mode
        n = 0
        for i in range(10):
            with struct.shuffle() as shuffler:
                ret = show(struct)
                if ret[0] != original[0]: n += 1
                assert ret[1] == original[1]
                with self.assertRaises(TypeError) as cm:
                    for i in shuffler: pass # should not be iterable
                self.assertIn('is not iterable', str(cm.exception))
        self.assertGreater(n, 5) # check at least 5 times different
        ret = show(struct)
        self.assertListEqual(ret[0], original[0])
        self.assertListEqual(ret[1], original[1])

        # test iteration
        with struct.shuffle(nr=100) as shuffler:
            c = 0
            n = 0
            for i in shuffler:
                self.assertEqual(i, c)
                ret = show(struct)
                if ret[0] != original[0]: n += 1
                self.assertListEqual(ret[1], original[1])
                c += 1
            self.assertEqual(c, 100)
            self.assertGreater(n, 5) # check at least 5 times different
        ret = show(struct)
        self.assertListEqual(ret[0], original[0])
        self.assertListEqual(ret[1], original[1])

    def test_labels(self):

        # check that empty labels are forbidden
        fas = """\
>sam1@pop1
AAAAAAAAAA
>sam2@pop1
AAAAAAAAAA
>sam3@pop1,pop2,pop3
AAAAAAAAAA
>sam4
AAAAAAAAAA
>sam5@pop1,
AAAAAAAAAA
>sam6@pop1
AAAAAAAAAA
>sam7@pop1,,pop3
AAAAAAAAAA
>sam8@pop1
AAAAAAAAAA
"""

        with self.assertRaises(IOError):
            aln = egglib.io.from_fasta_string(fas, alphabet=egglib.alphabets.DNA, labels=True)

        # repair the fasta
        fas = fas.replace(',\n', '\n')
        fas = fas.replace(',,', ',pop2,')

        # import repaired fasta
        aln = egglib.io.from_fasta_string(fas, alphabet=egglib.alphabets.DNA, labels=True)
        check = [ ('sam1', ['pop1']),
                  ('sam2', ['pop1']),
                  ('sam3', ['pop1','pop2','pop3']),
                  ('sam4', []),
                  ('sam5', ['pop1']),
                  ('sam6', ['pop1']),
                  ('sam7', ['pop1','pop2','pop3']),
                  ('sam8', ['pop1'])]
        self.assertListEqual([(seq.name, list(seq.labels)) for seq in aln], check)

        # attempt to set 0-length label
        with self.assertRaises(ValueError):
            aln[0].labels.append('')

        with self.assertRaises(ValueError):
            aln[0].labels[0] = ''

        # test None (automatic if level not specified / allowed in structure input only if only one item)
        d = {None: {None: {'i1': [0, 1], 'i2': [2, 3], 'i3': [6, 7], 'i4': [8, 9]}}}, {'i1': [10, 11]}
        struct = egglib.struct_from_dict(*d)
        dx = struct.as_dict()
        self.assertDictEqual(dx[0], d[0])
        self.assertDictEqual(dx[1], d[1])

        d = {'c1': {}, 'c2': {None: {'i1': [0, 1], 'i2': [2, 3], 'i3': [6, 7], 'i4': [8, 9]}}}, {'i1': [10, 11]}
        with self.assertRaises(ValueError):
            struct = egglib.struct_from_dict(*d)

        d = ({'c1': {None: {'i1': [0, 1], 'i2': [2, 3]}}}, {'i1': [4,5]})
        with self.assertRaises(ValueError):
            struct = egglib.struct_from_dict(*d)

        # check that non-represented levels are automatically set to a single None item
        aln = egglib.io.from_fasta_string("""\
>sam1@pop1
AAAAAAAAAA
>sam2@pop1
AAAAAAAAAA
>sam3@pop2
AAAAAAAAAA
>sam4@pop2
AAAAAAAAAA
>sam5@#
AAAAAAAAAA
>sam6@#
AAAAAAAAAA
""", alphabet=egglib.alphabets.DNA, labels=True)

        dx = egglib.struct_from_labels(aln, lvl_pop=0).as_dict()
        self.assertDictEqual(dx[0], {None: {'pop1': {'0': [0], '1': [1]}, 'pop2': {'2': [2], '3': [3]}}})
        self.assertDictEqual(dx[1], {'4': [4], '5': [5]})

        aln = egglib.io.from_fasta_string("""\
>sam1@i1
AAAAAAAAAA
>sam2@i1
AAAAAAAAAA
>sam3@i2
AAAAAAAAAA
>sam4@i2
AAAAAAAAAA
>sam5@#,i1
AAAAAAAAAA
>sam6@#,i1
AAAAAAAAAA
""", alphabet=egglib.alphabets.DNA, labels=True)

        dx = egglib.struct_from_labels(aln, lvl_indiv=0).as_dict()
        self.assertDictEqual(dx[0], {None: {None: {'i1': [0, 1], 'i2': [2, 3]}}})
        self.assertDictEqual(dx[1], {'i1': [4,5]})

        aln = egglib.io.from_fasta_string("""\
>sam1@c1,i1
AAAAAAAAAA
>sam2@c1,i1
AAAAAAAAAA
>sam3@c1,i2
AAAAAAAAAA
>sam4@c1,i2
AAAAAAAAAA
>sam5@#,i1
AAAAAAAAAA
>sam6@#,i1
AAAAAAAAAA
""", alphabet=egglib.alphabets.DNA, labels=True)

        dx = egglib.struct_from_labels(aln, lvl_clust=0, lvl_indiv=1).as_dict()
        self.assertDictEqual(dx[0], {'c1': {'c1': {'i1': [0, 1], 'i2': [2, 3]}}})
        self.assertDictEqual(dx[1], {'i1': [4,5]})

        # check outgroup sample
        dx = egglib.struct_from_labels(aln, lvl_clust=0, lvl_indiv=1, skip_outgroup=True).as_dict()
        self.assertDictEqual(dx[0], {'c1': {'c1': {'i1': [0, 1], 'i2': [2, 3]}}})
        self.assertDictEqual(dx[1], {})

        # support missing samples
        aln = egglib.io.from_fasta_string("""\
>sam1@idv1,pop1
AAAAAAAAAA
>sam2@idv2,pop1
AAAAAAAAAA
>sam3@idv3,pop1
AAAAAAAAAA
>sam4
AAAAAAAAAA
>sam5@idv4
AAAAAAAAAA
>sam6@idv5,pop2
AAAAAAAAAA
>sam7@idv6,pop2
AAAAAAAAAA
>sam8@#
AAAAAAAAAA
""", alphabet=egglib.alphabets.DNA, labels=True)

        dx = egglib.struct_from_labels(aln, lvl_indiv=0, lvl_pop=1).as_dict()
        self.assertDictEqual(dx[0], {None: {'pop1': {'idv1': [0], 'idv2': [1], 'idv3': [2]}, 'pop2': {'idv5': [5], 'idv6': [6]}}})
        self.assertDictEqual(dx[1], {})

        aln = egglib.io.from_fasta_string("""\
>sam1@idv1,pop1
AAAAAAAAAA
>sam2@idv2,pop1
AAAAAAAAAA
>sam3@idv3,pop1
AAAAAAAAAA
>sam4
AAAAAAAAAA
>sam5@idv4
AAAAAAAAAA
>sam6@idv5,pop2
AAAAAAAAAA
>sam7@idv6,pop2
AAAAAAAAAA
>sam8@#,idv1
AAAAAAAAAA
""", alphabet=egglib.alphabets.DNA, labels=True)

        dx = egglib.struct_from_labels(aln, lvl_indiv=0, lvl_pop=1).as_dict()
        self.assertDictEqual(dx[0], {None: {'pop1': {'idv1': [0], 'idv2': [1], 'idv3': [2]}, 'pop2': {'idv5': [5], 'idv6': [6]}}})
        self.assertDictEqual(dx[1], {'idv1': [7]})

    def test_outgroup_label(self):

        # structure with 2 pops + 1 `outgroup` single-indiv pop
        coal = egglib.coalesce.Simulator(3, num_indiv=[5, 5, 1], migr_matrix=[[None, 1, 0], [1, None, 0], [0, 0, None]])
        coal.params.add_event('merge', T=3, src=2, dst=0)
        coal.params.add_event('merge', T=3, src=1, dst=0)

        # perform a simulation
        aln = coal.simul()

        # shows the labels
        self.assertListEqual(list(aln[0].labels), ['0', '0'])
        self.assertListEqual(list(aln[1].labels), ['0', '0'])
        self.assertListEqual(list(aln[2].labels), ['0', '1'])
        self.assertListEqual(list(aln[3].labels), ['0', '1'])
        self.assertListEqual(list(aln[4].labels), ['0', '2'])
        self.assertListEqual(list(aln[5].labels), ['0', '2'])
        self.assertListEqual(list(aln[6].labels), ['0', '3'])
        self.assertListEqual(list(aln[7].labels), ['0', '3'])
        self.assertListEqual(list(aln[8].labels), ['0', '4'])
        self.assertListEqual(list(aln[9].labels), ['0', '4'])
        self.assertListEqual(list(aln[10].labels), ['1', '5'])
        self.assertListEqual(list(aln[11].labels), ['1', '5'])
        self.assertListEqual(list(aln[12].labels), ['1', '6'])
        self.assertListEqual(list(aln[13].labels), ['1', '6'])
        self.assertListEqual(list(aln[14].labels), ['1', '7'])
        self.assertListEqual(list(aln[15].labels), ['1', '7'])
        self.assertListEqual(list(aln[16].labels), ['1', '8'])
        self.assertListEqual(list(aln[17].labels), ['1', '8'])
        self.assertListEqual(list(aln[18].labels), ['1', '9'])
        self.assertListEqual(list(aln[19].labels), ['1', '9'])
        self.assertListEqual(list(aln[20].labels), ['2', '10'])
        self.assertListEqual(list(aln[21].labels), ['2', '10'])

        # make structure with three populations ignoring individual level
        ing, otg = egglib.struct_from_labels(aln, lvl_pop=0).as_dict()
        self.assertDictEqual(ing, {None: {
            '0': {    '0': [0],  '1': [1],   '2': [2],   '3': [3],   '4': [4],   '5': [5],   '6': [6],   '7': [7],   '8': [8],   '9': [9]},
            '1': {  '10': [10], '11': [11], '12': [12], '13': [13], '14': [14], '15': [15], '16': [16], '17': [17], '18': [18], '19': [19]},
            '2': {  '20': [20], '21': [21]}}})
        self.assertDictEqual(otg, {})

        # make structure with three populations
        ing, otg = egglib.struct_from_labels(aln, lvl_pop=0, lvl_indiv=1).as_dict()
        self.assertDictEqual(ing, {None: {
            '0': {  '0': [ 0, 1], '1': [ 2, 3], '2': [ 4, 5], '3': [ 6, 7], '4': [ 8, 9]},
            '1': {  '5': [10,11], '6': [12,13], '7': [14,15], '8': [16,17], '9': [18,19]},
            '2': { '10': [20,21]}}})
        self.assertDictEqual(otg, {})

        # two populations + outgroup ignoring individual level
        ing, otg = egglib.struct_from_labels(aln, lvl_pop=0, outgroup_label='2').as_dict()
        self.assertDictEqual(ing, {None: {
            '0': {    '0': [0],  '1': [1],   '2': [2],   '3': [3],   '4': [4],   '5': [5],   '6': [6],   '7': [7],   '8': [8],   '9': [9]},
            '1': {  '10': [10], '11': [11], '12': [12], '13': [13], '14': [14], '15': [15], '16': [16], '17': [17], '18': [18], '19': [19]}}})
        self.assertDictEqual(otg, {'20': [20], '21': [21]})

        # two populations + outgroup
        ing, otg = egglib.struct_from_labels(aln, lvl_pop=0, lvl_indiv=1, outgroup_label='2').as_dict()
        self.assertDictEqual(ing, {None: {
            '0': {  '0': [ 0, 1], '1': [ 2, 3], '2': [ 4, 5], '3': [ 6, 7], '4': [ 8, 9]},
            '1': {  '5': [10,11], '6': [12,13], '7': [14,15], '8': [16,17], '9': [18,19]}}})
        self.assertDictEqual(otg, {'10': [20,21]})

    def test_from_samplesizes(self):
        struct = egglib.struct_from_samplesizes([5, 5], ploidy=2, outgroup=1)
        ref = ({None:
                {'pop1': {'idv1': [0, 1], 'idv2': [2, 3], 'idv3': [4, 5],
                          'idv4': [6, 7], 'idv5': [8, 9]},
                 'pop2': {'idv6': [10, 11], 'idv7': [12, 13],
                          'idv8': [14, 15], 'idv9': [16, 17],
                          'idv10': [18, 19]}}}, {'idv11': [20, 21]})
        self.assertTupleEqual(struct.as_dict(), ref)

        self.assertTupleEqual(egglib.struct_from_samplesizes([6], ploidy=1, outgroup=0).as_dict(), ({
            None: {'pop1': {'idv1': [0], 'idv2': [1], 'idv3': [2], 'idv4': [3], 
                    'idv5': [4], 'idv6': [5]}}}, {}))

        self.assertTupleEqual(egglib.struct_from_samplesizes([], ploidy=4, outgroup=2).as_dict(), ({
            None: {}}, {'idv1': [0, 1, 2, 3], 'idv2': [4, 5, 6, 7]}))

        self.assertTupleEqual(egglib.struct_from_samplesizes([4, 1, 0, 2], ploidy=3, outgroup=2).as_dict(), (
            {None: {
                'pop1': {'idv1': [0, 1, 2], 'idv2': [3, 4, 5], 'idv3': [6, 7, 8], 'idv4': [9, 10, 11]},
                'pop2': {'idv5': [12, 13, 14]},
                'pop3': {},
                'pop4': {'idv6': [15, 16, 17], 'idv7': [18, 19, 20]}}},
            {'idv8': [21, 22, 23], 'idv9': [24, 25, 26]}))

        self.assertTupleEqual(egglib.struct_from_samplesizes([0], ploidy=1, outgroup=0).as_dict(), ({None: {'pop1': {}}}, {}))

        self.assertTupleEqual(egglib.struct_from_samplesizes([], ploidy=1, outgroup=0).as_dict(), ({None: {}}, {}))
