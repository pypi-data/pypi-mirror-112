import os, egglib, sys, unittest, random, re, gc, time
from collections import Iterable
path = os.path.dirname(__file__)
path_T=os.path.join(path, 'correct_files')
path_F=os.path.join(path, 'erroneous_files')

class Codeml_test(unittest.TestCase):

    def test_codeml_T(self):
        cds = egglib.Align.create([
            ('UEOg7RZXzI', 'TGCTCAAAAATCATGAAAAAACGTAAATCTAGAGTTGGTCCAATTGATCTCAGGCATAGGAATTTGCCC'),
            ('Cx5JVJRSVu', 'TGCTCCAAAATCATGAAAAAACGTAAATCTAGAGTTGGTCCAATTGATCTCAGGCATAGGAATTTGCCC'),
            ('D6076jpYM1', 'TGCTCAGAAATCATGAAAAAAAGGAAATCTAGAGTTGGTCCAATTGATCTCAGGCATAGGAATTTGCCC'),
            ('D8GDCiy9Ov', 'TGCTCAACAATCATGAAAAAAAGGAAATCTAGAGTTGGTCCAATTGATCTCAGGCATAGGAATTTGCCC'),
            ('Sg4P4pwoAD', 'TGCTCAAATATCATGAAAAAACGTAAATCTAGAGTTGGTCCAATTGATCTCAGGCATAGGAATTTGCCC'),
            ('GVj_VDpGcX', 'TGCTCAAAAGTCATGAAAAAACGTAAATCTAGAGTTGGTCCAATTGATCTCAGGCATAGGAATTTGCCC')],
            egglib.alphabets.DNA)
        cds.to_codons()
        CML_results=egglib.wrappers.codeml(align=cds, tree=None, model='M0', verbose=False)
        self.assertIsInstance(CML_results, dict)
        self.assertEqual(CML_results['np'], 8)
        self.assertEqual(CML_results['lnL'], -139.282532)
        self.assertAlmostEqual(CML_results['length'], 0.463337, places=4)

        tree0, stats = egglib.wrappers.phyml(cds, model='HKY85', verbose=False, boot=1)
        CML_resultsT = egglib.wrappers.codeml(align=cds, tree=None, model='M0')
        self.assertIsInstance(CML_resultsT['tree'], egglib._tree.Tree)

    def test_codeml_E(self):
        cache = egglib.wrappers.paths['codeml']
        egglib.wrappers.paths['codeml'] = None
        cds = egglib.io.from_fasta(os.path.join(path_T, 'codon_align.fas'), egglib.alphabets.DNA)
        cds = cds.subset(range(6))
        cds = cds.extract(0, 69)
        cds.encode() # this simulated fasta has no names
        with self.assertRaises(RuntimeError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M0')
        egglib.wrappers.paths['codeml'] = cache

        cnt=egglib.io.from_fasta(os.path.join(path_T, 'codon_align.fas'), egglib.alphabets.DNA, cls=egglib.Container)
        with self.assertRaises(TypeError):
            egglib.wrappers.codeml(align=cnt, tree=None, model='M0')

        cds = egglib.io.from_fasta(os.path.join(path_F, 'cds_e.fas'), egglib.alphabets.DNA)
        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M0')

        cds = egglib.io.from_fasta(os.path.join(path_T, 'codon_align.fas'), egglib.alphabets.DNA)
        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M0', code=12)
        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M0', code='error')

        cds = egglib.io.from_fasta(os.path.join(path_F, 'example_ename.fas'), egglib.alphabets.DNA)
        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M0')

        cds = egglib.io.from_fasta(os.path.join(path_F, 'example_edpl.fas'), egglib.alphabets.DNA)
        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M0')

        cds = egglib.io.from_fasta(os.path.join(path_F, 'codon_align_cstop.fas'), egglib.alphabets.DNA)
        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M0')

        cds = egglib.io.from_fasta(os.path.join(path_T, 'cds_clust.fas'), egglib.alphabets.DNA)
        cds = cds.subset(range(6))
        cds = cds.extract(0, 69)
        cds.encode()
        cds.to_codons()

        tree = egglib.Tree(string='(Spider:0.01257025,Woolly:0.02023601,(Howler:0.03625789,((Titi:0.02002846,Saki:0.02646824):0.01312676)));')
        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=tree, model='M0')
        tree = egglib.Tree()
        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=tree, model='M0')

        tree =egglib.Tree(string=   '(Poplar_LG_VIII_pseudogene:0.30137798,Oryza:0.45654019,(Lotus:0.2258327,(Medicago:0.05478729,(Vitis:0.12466652,Poperrorlar_LG_X:0.00790383)1:0.07276364)1:0.07673733)1:0.13170743);')
        with self.assertRaises(NameError): #``NameError`` raised instead a ``ValueError`` line:395 in _codeml.py
            egglib.wrappers.codeml(align=cds, tree=tree, model='M0')

        #Test on error with the tree parameter is not finished

        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='error')

        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='D', ncat=5)

        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M7', ncat=None)

        with self.assertRaises(TypeError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M7', ncat='error')

        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M7', ncat=1)

        #Test on error with the req_tags and tags parameter is not finished

        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M0', codon_freq=8)

        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M0', kappa=-10)

        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M0', omega=-10)

        with self.assertRaises(ValueError):
            egglib.wrappers.codeml(align=cds, tree=None, model='M7', omega=0.90)

    def test_alphabets(self):
        base = egglib.Align.create([
            ('UEOg7RZXzI', ['TGC','TCA','AAA','ATC','ATG','AAA','AAA','CGT','AAA','TCT','AGA','GTT','GGT','CCA','ATT','GAT','CTC','AGG','CAT','AGG','AAT','TTG','CCC']),
            ('Cx5JVJRSVu', ['TGC','TCC','AAA','ATC','ATG','AAA','AAA','CGT','AAA','TCT','AGA','GTT','GGT','CCA','ATT','GAT','CTC','AGG','CAT','AGG','AAT','TTG','CCC']),
            ('D6076jpYM1', ['TGC','TCA','GAA','ATC','ATG','AAA','AAA','AGG','AAA','TCT','AGA','GTT','GGT','CCA','ATT','GAT','CTC','AGG','CAT','AGG','AAT','TTG','CCC']),
            ('D8GDCiy9Ov', ['TGC','TCA','ACA','ATC','ATG','AAA','AAA','AGG','AAA','TCT','AGA','GTT','GGT','CCA','ATT','GAT','CTC','AGG','CAT','AGG','AAT','TTG','CCC']),
            ('Sg4P4pwoAD', ['TGC','TCA','AAT','ATC','ATG','AAA','AAA','CGT','AAA','TCT','AGA','GTT','GGT','CCA','ATT','GAT','CTC','AGG','CAT','AGG','AAT','TTG','CCC']),
            ('GVj_VDpGcX', ['TGC','TCA','AAA','GTC','ATG','AAA','AAA','CGT','AAA','TCT','AGA','GTT','GGT','CCA','ATT','GAT','CTC','AGG','CAT','AGG','AAT','TTG','CCC'])],
            egglib.alphabets.codons)

        CML_results=egglib.wrappers.codeml(align=base, tree=None, model='M0', verbose=False)
        self.assertIsInstance(CML_results, dict)
        self.assertEqual(CML_results['np'], 8)
        self.assertEqual(CML_results['lnL'], -139.282532)
        self.assertAlmostEqual(CML_results['length'], 0.463337, places=4)
