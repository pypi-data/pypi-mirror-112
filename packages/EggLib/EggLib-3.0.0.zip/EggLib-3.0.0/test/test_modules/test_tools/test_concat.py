import os, egglib, sys, unittest, random, re, gc, time
from collections import Iterable
path = os.path.dirname(__file__)
path_T=os.path.join(path, 'correct_files')
path_F=os.path.join(path, 'erroneous_files')

class Concat_test(unittest.TestCase):
    def test_concat_T(self):
        fname1='c_file_1.1.fsa' 
        fname2='c_file_2.fsa' 
        aln1= egglib.io.from_fasta(os.path.join(path_T,fname1), labels=False, cls=egglib._interface.Align, alphabet=egglib.alphabets.DNA)
        aln2= egglib.io.from_fasta(os.path.join(path_T,fname2), labels=False, cls=egglib._interface.Align, alphabet=egglib.alphabets.DNA)
        aln3=egglib.tools.concat(aln1,aln2)
        self.assertIsInstance(aln3, egglib.Align)
        self.assertEqual(aln3.ns, 10)
        self.assertEqual(aln3.ls, 720)

    def test_concat_E(self):
        fname1='c_file_1.1.fsa' 
        fname2='c_file_2.fsa' 
        fname3='c_file_1.fsa' 
        aln1= egglib.io.from_fasta(os.path.join(path_T,fname1), labels=False, cls=egglib._interface.Align, alphabet=egglib.alphabets.DNA)
        aln2= egglib.io.from_fasta(os.path.join(path_T,fname2), labels=False, cls=egglib._interface.Align, alphabet=egglib.alphabets.DNA)
        cnt3= egglib.io.from_fasta(os.path.join(path_T,fname2), labels=False, cls=egglib._interface.Container, alphabet=egglib.alphabets.DNA)

        with self.assertRaises(ValueError):
            egglib.tools.concat(aln1, aln2, fail=True)
        with self.assertRaises(TypeError):
            egglib.tools.concat(aln1, cnt3)
        with self.assertRaises(ValueError):
            egglib.tools.concat(aln1,aln2, space= -10)
        with self.assertRaises(ValueError):
            egglib.tools.concat(aln1, aln2, space=[1,2,3,4,5,6,7,8,9,-10])
        with self.assertRaises(ValueError):
            egglib.tools.concat(aln1, aln2, space=[1,2,3,4,5,6,7,8,9,10,11,12,13,14])
        with self.assertRaises(ValueError):
            egglib.tools.concat(aln1,aln2, ch='^^' )
        with self.assertRaises(ValueError):
            aln1.del_sample(0)
            egglib.tools.concat(aln1, aln2,ignore_names=True)
        with self.assertRaises(ValueError):	
            egglib.tools.concat(aln1,aln2, no_missing=True)

        aln4= egglib.Align(egglib.alphabets.DNA)
        aln5= egglib.Align(egglib.alphabets.DNA)
        aln6= egglib.Align(egglib.alphabets.DNA)
        aln4.ng=2
        aln5.ng=2
        aln6.ng=3
        aln4.add_samples([('name1', 'GAAAAAAAAGGAA', ['0','0']), ('name2', 'AAGAAAGCGAGTG', ['0','0']), ('name3', 'AAGCTTGCGGGTG', ['0','1']), ('name4', 'CCCAAAGCGAGTG', ['0','1']), ('name5', 'AAGCTTGCGAGTG', ['0','1']), ('name6', 'GAAAAAGTCAAAA', ['1','2']), ('name7', 'GAAAAAAAAAAAG', ['1','2']), ('name8', 'GAAACCCAAAAAA', ['1','2']), ('name9', 'AGCGTTTTGCGTG', ['1','2']), ('name10', 'CAGCGTTGAGCGT', ['1','2']),('name11', 'AGCGTCCGGTCGT', ['1','1'])])
        aln5.add_samples([('name1', 'GAAAAAAAAGGAA'), ('name2', 'AAGAAAGCGAGTG'), ('name3', 'AAGCTTGCGGGTG'), ('name4', 'CCCAAAGCGAGTG'), ('name5', 'AAGCTTGCGAGTG'), ('name6', 'GAAAAAGTCAAAA'), ('name7', 'GAAAAAAAAAAAG'), ('name8', 'GAAACCCAAAAAA'), ('name9', 'AGCGTTTTGCGTG'), ('name10', 'CAGCGTTGAGCGT'),('name11', 'AGCGTCCGGTCGT')])
        aln6.add_samples([('name1', 'GAAAAAAAAGGAA', ['0','0','0']), ('name2', 'AAGAAAGCGAGTG', ['0','0','1']), ('name3', 'AAGCTTGCGGGTG', ['0','1','0']), ('name4', 'CCCAAAGCGAGTG', ['0','1','1']), ('name5', 'AAGCTTGCGAGTG', ['0','1','0']), ('name6', 'GAAAAAGTCAAAA', ['1','2','0']), ('name7', 'GAAAAAAAAAAAG', ['1','2','1']), ('name8', 'GAAACCCAAAAAA', ['1','2','0']), ('name9', 'AGCGTTTTGCGTG', ['1','2','1']), ('name10', 'CAGCGTTGAGCGT', ['1','2','0']),('name11', 'AGCGTCCGGTCGT', ['1','0','1'])])

        with self.assertRaises(ValueError):
            egglib.tools.concat(aln4,aln5, group_check=True)
        with self.assertRaises(ValueError):
            egglib.tools.concat(aln5,aln6, group_check=True)

        aln7= egglib.Align(egglib.alphabets.DNA)
        aln7.add_sample('name1', 'ACCGCCGGGAAAAA')
        aln7.add_sample('name2', 'CCCGTTGCGCAAAA')
        aln8= egglib.Align(egglib.alphabets.protein)
        aln8.add_sample('name1', 'MGGGCAGLTALS')
        aln8.add_sample('name2', 'MGTSSSLACTAL')
        with self.assertRaises(ValueError):
            egglib.tools.concat(aln7, aln8)

        fname1='c_file_1.1.fsa' 
        fname2='c_file_2.fsa' 
        aln1 = egglib.io.from_fasta(os.path.join(path_T,fname1), labels=False, cls=egglib._interface.Align, alphabet=egglib.alphabets.DNA)
        aln2 = egglib.io.from_fasta(os.path.join(path_T,fname2), labels=False, cls=egglib._interface.Align, alphabet=egglib.alphabets.DNA)
        aln3 = egglib.Align.create(list(aln2),
                    alphabet=egglib.alphabets.Alphabet('char', 'ACGT', '-'))

        with self.assertRaises(ValueError):
            aln4=egglib.tools.concat(aln1, aln3, aln2)
