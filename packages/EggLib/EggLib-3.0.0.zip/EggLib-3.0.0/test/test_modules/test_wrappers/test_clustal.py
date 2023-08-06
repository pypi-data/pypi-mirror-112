import os, egglib, sys, unittest, random, re, gc, time
from collections import Iterable
path = os.path.dirname(__file__)
path_T=os.path.join(path, 'correct_files')
path_F=os.path.join(path, 'erroneous_files')


class Clustal_test(unittest.TestCase):
    def test_clustal_T(self):
        cnt = egglib.io.from_fasta(os.path.join(path_T, 'cds.fas'), egglib.alphabets.DNA, labels=True)
        aln = egglib.wrappers.clustal(cnt, verbose=False, threads=8, keep_order=True)
        aln.fasta(fname='after_clustal')
        Lts_cnt=cnt.find('Lotus')
        Lts_aln=aln.find('Lotus')
        seq_cnt=Lts_cnt.sequence.string()
        seq_aln=Lts_aln.sequence.string()
        seq_=seq_aln.replace("-","")
        n_miss=seq_aln.count('-')
            
        self.assertIsInstance(aln, egglib.Align)
        self.assertNotEqual(len(seq_cnt), len(seq_aln))
        self.assertEqual(len(seq_cnt), (len(seq_aln)-n_miss))
        self.assertEqual(seq_, seq_cnt)
        os.remove('after_clustal')
        

    def test_clustal_E(self):
        cnt = egglib.io.from_fasta(os.path.join(path_T, 'cds.fas'), egglib.alphabets.DNA, labels=True)
        cache = egglib.wrappers.paths['clustal']
        egglib.wrappers.paths['clustal'] = None
        with self.assertRaises(RuntimeError):
            aln = egglib.wrappers.clustal(cnt, verbose=False, threads=8, keep_order=True)
        egglib.wrappers.paths['clustal'] = cache

        cnt_ref = egglib.io.from_fasta(os.path.join(path_T, 'cds.fas'), egglib.alphabets.DNA, cls=None)
        with self.assertRaises(TypeError):
            aln = egglib.wrappers.clustal(cnt, ref=cnt_ref, verbose=False, threads=8, keep_order=True)

        aln_e = egglib.io.from_fasta(os.path.join(path_F, 'error.fas'), egglib.alphabets.DNA, cls=egglib.Align) #empty file
        with self.assertRaises(ValueError):
            aln = egglib.wrappers.clustal(cnt_ref, ref=aln_e, verbose=False, threads=8, keep_order=True)
        
        cnt=egglib.io.from_fasta(os.path.join(path_F, 'cds_e.fas'), egglib.alphabets.DNA, labels=True)
        with self.assertRaises(ValueError):
            aln = egglib.wrappers.clustal(cnt, verbose=False, threads=8, keep_order=True)
        
        aln_e = egglib.io.from_fasta(os.path.join(path_F, 'error.fas'), egglib.alphabets.DNA, cls=egglib.Align) #empty file
        with self.assertRaises(ValueError):
            aln = egglib.wrappers.clustal(aln_e, verbose=False, threads=8, keep_order=True)

        aln_ref = egglib.io.from_fasta(os.path.join(path_T, 'cds_clust.fas'), egglib.alphabets.DNA, cls=egglib.Align) #empty file
        with self.assertRaises(ValueError):
            aln = egglib.wrappers.clustal(aln_e, ref=aln_ref, verbose=False, threads=8, keep_order=True)

        Lts_cnt=['e', 'r', 'r', 'o', 'r']
        with self.assertRaises(AttributeError):
            aln = egglib.wrappers.clustal(Lts_cnt,verbose=False, threads=8, keep_order=True)

        cnt = egglib.io.from_fasta(os.path.join(path_T, 'cds.fas'), egglib.alphabets.DNA, labels=True)

        with self.assertRaises(ValueError):
                aln= egglib.wrappers.clustal(cnt,verbose=False, threads=8, use_kimura=True, keep_order=True)
        
        with self.assertRaises(ValueError):
                aln= egglib.wrappers.clustal(cnt ,verbose=False, num_iter=-10, threads=8)

        with self.assertRaises(ValueError):
                aln= egglib.wrappers.clustal(cnt ,verbose=False, num_iter='100', threads=8)

        with self.assertRaises(ValueError):
                aln= egglib.wrappers.clustal(cnt ,verbose=False, threads=-8)


        aln_ref = egglib.io.from_fasta(os.path.join(path_T, 'codon_align.fas'), egglib.alphabets.DNA)
        with self.assertRaises(RuntimeError):
            aln = egglib.wrappers.clustal(cnt, ref=aln_ref, verbose=False, threads=8, keep_order=True)
