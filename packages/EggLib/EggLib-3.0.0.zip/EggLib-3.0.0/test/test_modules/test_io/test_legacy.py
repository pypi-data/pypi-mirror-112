import os, egglib, sys, unittest, random, re, gc, time
from collections import Iterable
path = os.path.dirname(__file__)
path_T=os.path.join(path, 'correct_files')
path_F=os.path.join(path, 'erroneous_files')


class Legacy_test(unittest.TestCase):
    #test on the method "from_clustal"
    def test_from_clustal_T(self):
        fname='align.aln'
        string = open(os.path.join(path_T,fname)).read()
        aln=egglib.io.from_clustal(string, egglib.alphabets.protein)
        self.assertIsInstance(aln, egglib._interface.Align)

    def test_from_clustal_E(self):
        fname='clustal_error1.aln'
        string = open(os.path.join(path_F,fname)).read()
        with self.assertRaises(ValueError): #file with an error at the first line: without CLUSTAL...
            aln=egglib.io.from_clustal(string, egglib.alphabets.protein)

        fname='clustal_error2.aln'
        string = open(os.path.join(path_F,fname)).read()
        with self.assertRaises(ValueError): #file with space before each lines
            aln=egglib.io.from_clustal(string, egglib.alphabets.protein)

        fname='clustal_error3.aln'
        string = open(os.path.join(path_F,fname)).read()
        with self.assertRaises(ValueError): #file without conservation line for the first alignment
            aln=egglib.io.from_clustal(string, egglib.alphabets.protein)

        fname='clustal_error4.aln'
        string = open(os.path.join(path_F,fname)).read()
        with self.assertRaises(ValueError): #file with more than 3 blocks
            aln=egglib.io.from_clustal(string, egglib.alphabets.protein)

        fname='clustal_error5.aln'
        string = open(os.path.join(path_F,fname)).read()
        with self.assertRaises(ValueError): #file with fakes base numbers .
            aln=egglib.io.from_clustal(string, egglib.alphabets.protein)

        fname='clustal_error6.aln'
        string = open(os.path.join(path_F,fname)).read()
        with self.assertRaises(ValueError): #file with string like base numbers .
            aln=egglib.io.from_clustal(string, egglib.alphabets.protein)

        fname='clustal_error7.aln'
        string = open(os.path.join(path_F,fname)).read()
        with self.assertRaises(ValueError): #file with string like base numbers .
            aln=egglib.io.from_clustal(string, egglib.alphabets.protein)

        fname='clustal_error8.aln'
        string = open(os.path.join(path_F,fname)).read()
        with self.assertRaises(ValueError): #error on next line.
            aln=egglib.io.from_clustal(string, egglib.alphabets.protein)

        with self.assertRaises(ValueError):
            aln=egglib.io.from_clustal(string, egglib.alphabets.codons)
        bidon = egglib.alphabets.Alphabet('char', '01', 'N', name='binary')
        with self.assertRaises(ValueError):
            aln=egglib.io.from_clustal(string, bidon)
        with self.assertRaises(ValueError):
            aln=egglib.io.from_clustal(string, egglib.alphabets.DNA)

    #test on the method "from_staden"
    def test_from_staden_T(self):
        fname='example.sta'
        string = open(os.path.join(path_T, fname)).read()
        stn=egglib.io.from_staden(string,keep_consensus=True)
        stn2=egglib.io.from_staden(string,keep_consensus=False)
        self.assertIsInstance(stn, egglib._interface.Align)
        self.assertIn("CONSENSUS", stn)
        self.assertNotIn("CONSENSUS", stn2)

    def test_from_staden_E(self):
        fname='example_E.sta'
        string = open(os.path.join(path_F, fname)).read()
        with self.assertRaises(ValueError): #file with an error at the first line: without CLUSTAL...
            stn=egglib.io.from_staden(string,keep_consensus=True)

    #test on the method "from_genalys"
    def test_from_genalys_T(self):
        fname='example.gnl'
        string = open(os.path.join(path_T, fname)).read()
        gnl=egglib.io.from_genalys(string)
        self.assertEqual(str(type(gnl)), "<class 'egglib._interface.Align'>")
        self.assertEqual(gnl.get_name(0),'L0738D_HM55_Leg196F_F10_070.ab1')
        self.assertTrue(gnl.ns >0)
    
    #test on the method "get_fgenesh"
    def test_get_fgenesh_T(self):
        fname='example.fg'
        string = open(os.path.join(path_T,fname)).read()
        fgh=egglib.io.get_fgenesh(string)
        self.assertIsInstance(fgh, list)
        self.assertTrue (len(fgh)>0) #1522 
        
    def test_get_fgenesh_E(self):
        fname='example_E.fg'
        string = open(os.path.join(path_F,fname)).read()
        with self.assertRaises(ValueError): 
            fgh=egglib.io.get_fgenesh(string)

        fname='example_E2.fg'
        string = open(os.path.join(path_F,fname)).read()
        with self.assertRaises(ValueError): 
            fgh=egglib.io.get_fgenesh(string)

        fname='example_E3.fg'
        string = open(os.path.join(path_F,fname)).read()
        with self.assertRaises(ValueError): 
            fgh=egglib.io.get_fgenesh(string)





