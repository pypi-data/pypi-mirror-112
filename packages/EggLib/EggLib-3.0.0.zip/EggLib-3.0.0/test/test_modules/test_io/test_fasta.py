import os, egglib, sys, unittest, random, re, gc, time
from collections import Iterable
path = os.path.dirname(__file__)
path_T=os.path.join(path, 'correct_files')
path_F=os.path.join(path, 'erroneous_files')

class Fasta_test(unittest.TestCase):
    def test_from_fasta_T(self):
        fname_T='align1_T.fas'
        aln = egglib.io.from_fasta(os.path.join(path_T,fname_T), egglib.alphabets.DNA)
        self.assertIsInstance(aln, egglib.Align)
        self.assertEqual(aln.ns, 101)
        self.assertEqual(aln.ls, 8942)

    def test_from_fasta_E(self):
        fname_T='align1_T.fas'
        fname_F='align1_F.fas'
        with self.assertRaises(ValueError):
            aln = egglib.io.from_fasta(os.path.join(path_T,fname_T), egglib.alphabets.DNA, labels=False, cls='LOL') 
            #an error integrated in the "cls" parameter
        with self.assertRaises(ValueError):
            aln = egglib.io.from_fasta(os.path.join(path_F,fname_F), egglib.alphabets.DNA, labels=False, cls='Align') 
            #The file 'align1_E.fs', contains sequences of differents sizes

    def setUp(self):
        fname='align1_T.fas'
        self.iter_aln=egglib.io.fasta_iter(os.path.join(path_T,fname), egglib.alphabets.DNA)

    def tearDown(self):
        del self.iter_aln

    def test_fasta_iter_T(self):
        self.assertIsInstance(self.iter_aln, egglib.io.fasta_iter)
        self.assertIsInstance(self.iter_aln, Iterable)

    def test__enter__T(self):
        with self.iter_aln as iter_aln:
            self.assertIsInstance(iter_aln, egglib.io.fasta_iter)

    def test__exit__T(self):
        ext=self.iter_aln.__exit__(None, None, None)
        self.assertFalse(ext)
        with self.assertRaises(StopIteration):
            next(self.iter_aln)

    def test__iter__T(self):
        self.assertIsInstance(self.iter_aln, Iterable)

    def test_next_T(self):
        self.assertIsInstance(next(self.iter_aln), egglib._interface.SampleView)

    def test_next_E(self):
        fname_E='align1_E.fas'
        iter_alnE=egglib.io.fasta_iter(os.path.join(path_F,fname_E), egglib.alphabets.DNA, True)
        with self.assertRaises(StopIteration):
            next(iter_alnE)
