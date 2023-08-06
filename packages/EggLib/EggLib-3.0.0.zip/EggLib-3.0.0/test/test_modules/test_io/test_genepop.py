import unittest, os, egglib

pathT = os.path.join(os.path.dirname(__file__), 'correct_files')
pathE = os.path.join(os.path.dirname(__file__), 'erroneous_files')

genepop1 = \
[[['AA8', '0405',' 0711', '0304', '0000', '0505'],
  ['AA9', '0405',' 0609', '0208', '0000', '0505'], 
  ['A10', '0205',' 0609', '0101', '0000', '0305'],
  ['A11', '0405',' 0606', '0002', '0000', '0504'],
  ['A12', '0202', '0609', '0105', '0000', '0507'],
  ['A13', '0505', '0909', '0100', '0000', '0505'],
  ['A14', '0202', '0609', '0207', '0000', '0503'],
  ['A15', '0405', '0609', '0101', '0000', '0505']],

 [['AF', '0000', '0000', '0000', '0000','0505'],
  ['AF', '0205', '0307', '0102', '0000','0505'],
  ['AF', '0202', '0609', '0202', '0000','0505'],
  ['AF', '0205', '0909', '0000', '0000','0505'],
  ['AF', '0205', '0307', '0202', '0000','0505'],
  ['AF', '0505', '0303', '0102', '0000','0505'],
  ['AF', '0205', '0700', '0000', '0000','0505'],
  ['AF', '0505', '0900', '0000', '0000','0405'],
  ['AF', '0205', '0600', '0000', '0000','0505'],
  ['AF', '0505', '0606', '0202', '0000','0505']],

 [['C45', '0505',' 0606', '0202', '0000','0505'],
  ['C45', '0505',' 0909', '0202', '0000','0505'],
  ['C45', '0505',' 0306', '0202', '0000','0505'],
  ['C45', '0505',' 0909', '0102', '0000','0405'],
  ['C45', '0205',' 0303', '0202', '0000','0505'],
  ['C45', '0205',' 0909', '0202', '0000','0405']]]

genepop2 = \
[[['RueDuQuai',  '250230', '564568', '110100'],
  ['RueDuQuai',  '252238', '568558', '100120'],
  ['RueDuQuai',  '254230', '564558', '090100'],
  ['RueDuQuai',  '250230', '564568', '110100'],
  ['RueDuQuai',  '252240', '568558', '100120'],
  ['RueDuQuai',  '254230', '564558', '090090']],

 [['Benitier',   '254230', '564558', '080100'],
  ['Benitier',   '000230', '564558', '090080'],
  ['Benitier',   '254230', '000000', '090100'],
  ['Benitier',   '254230', '564000', '090120']]]



class Genepop_test(unittest.TestCase):

    def check(self, data, n, aln):
        c = 0
        for i, pop in enumerate(data):
            for idv in pop:
                self.assertEqual(aln[c].name, idv[0]+'_1')
                self.assertListEqual(list(aln[c].sequence), [int(i.strip()[:n]) for i in idv[1:]])
                self.assertListEqual(list(aln[c].labels), ['pop{0}'.format(i+1), idv[0]])
                self.assertEqual(aln[c+1].name, idv[0]+'_2')
                self.assertListEqual(list(aln[c+1].sequence), [int(i.strip()[n:]) for i in idv[1:]])
                self.assertListEqual(list(aln[c+1].labels), ['pop{0}'.format(i+1), idv[0]])
                c += 2

    def test_genepop_E(self):
        with self.assertRaises(IOError):
            egglib.io.from_genepop('I don\'t exist!')
        with self.assertRaises(ValueError):
            egglib.io.from_genepop(os.path.join(pathE, 'genepop0.txt'))

    def test_genepop_G(self):
        aln1 = egglib.io.from_genepop(os.path.join(pathT, 'genepop1.txt'))
        self.assertIsInstance(aln1, egglib.Align)

        aln2 = egglib.io.from_genepop(os.path.join(pathT, 'genepop2.txt'))
        self.assertIsInstance(aln2, egglib.Align)

        self.assertEqual(aln1.title, 'Microsat on Chiracus radioactivus, a pest species')
        self.assertListEqual(aln1.loci, ['Loc1', 'Loc2', 'Loc3', 'Y-linked', 'Loc4'])
        self.check(genepop1, 2, aln1)

        self.assertEqual(aln2.title, 'Title line: "Mosquito populations in southern France"')
        self.assertListEqual(aln2.loci, ['MicroSat 1', 'Microsat 2', 'Est-3'])
        self.check(genepop2, 3, aln2)
