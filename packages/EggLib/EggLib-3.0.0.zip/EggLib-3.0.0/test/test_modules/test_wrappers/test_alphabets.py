import unittest, os
import egglib
path = os.path.dirname(__file__)
path_T=os.path.join(path, '..', 'test_stats', 'control_stats')

class AlphabetAlign_test(unittest.TestCase):

    def test_align(self):

        seq = egglib.io.from_fasta(os.path.join(path_T, 'FTLa.fas'), egglib.alphabets.DNA, labels=True)
        framepos = [(122, 323), (451, 513), (749, 789)]
        frame = egglib.tools.ReadingFrame(framepos) # remove 1 base of last exon to cause an error
        cds1 = egglib.tools.to_codons(seq, frame=frame)
        with self.assertRaises(ValueError): egglib.tools.to_codons(seq) # not a multiple of 3
        egglib.tools.to_codons(seq.extract(0, 1809))

        # check muscle and clustal
        with self.assertRaises(ValueError): egglib.wrappers.clustal(cds1)
        with self.assertRaises(ValueError): egglib.wrappers.muscle(cds1)
        aln = egglib.wrappers.clustal(seq, verbose=False)
        aln = egglib.wrappers.muscle(seq, verbose=False)
