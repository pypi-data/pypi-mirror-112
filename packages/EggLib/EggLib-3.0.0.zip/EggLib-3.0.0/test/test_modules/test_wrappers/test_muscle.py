import os, egglib, sys, unittest, random, re, gc, time
from collections import Iterable
path = os.path.dirname(__file__)
path_T=os.path.join(path, 'correct_files')
path_F=os.path.join(path, 'erroneous_files')

class Muscle_test(unittest.TestCase):
    
    def test_muscle_T(self):
        aln = egglib.io.from_fasta(os.path.join(path_T, 'cds.fas'), egglib.alphabets.DNA, labels=True)
        cnt = egglib.io.from_fasta(os.path.join(path_T, 'cds.fas'), egglib.alphabets.DNA, labels=True)
        for i in cnt:
            if i.ls%3!=0: i.sequence = i.sequence[:i.ls//3*3]
        cnt.to_codons()
        prot = egglib.tools.translate(cnt)
        aln0=egglib.wrappers.muscle(aln, verbose=False)
        aln1=egglib.wrappers.muscle(aln, verbose=False)
        aln2=egglib.wrappers.muscle(aln, verbose=False, maxiters=1, diags=True)
        aln3=egglib.wrappers.muscle(aln, maxiters=1, diags=True, seqtype='dna',
                        aa_profile='sv', distance1='kbit20_3')
        aln4=egglib.wrappers.muscle(prot, seqtype='protein', aa_profile='sv')
        aln5=egglib.wrappers.muscle(prot, seqtype='protein', aa_profile='le',
                    brenner=True, diags1=True, SUEFF=0.4, anchorspacing=5,
                    center=-1.9, diaglength=17, distance1='kmer20_4',
                    gapopen=-2.5, maxtrees=2, objscore='ps', smoothscoreceil=3.4,
                    weight1='henikoff')

        self.assertIsInstance(aln0, egglib.Align)
        self.assertIsInstance(aln1, egglib.Align)
        self.assertIsInstance(aln2, egglib.Align)
        self.assertIsInstance(aln3, egglib.Align)
        self.assertIsInstance(aln4, egglib.Align)
        self.assertIsInstance(aln5, egglib.Align)


    def test_muscle_E(self):
        cache = egglib.wrappers.paths['muscle']
        egglib.wrappers.paths['muscle']=None
        dna = egglib.io.from_fasta(os.path.join(path_T, 'cds.fas'), egglib.alphabets.DNA, labels=True)
        cnt = egglib.io.from_fasta(os.path.join(path_T, 'cds.fas'), egglib.alphabets.DNA, labels=True)
        for i in cnt:
            if i.ls%3!=0: i.sequence = i.sequence[:i.ls//3*3]
        cnt.to_codons()
        prot = egglib.tools.translate(cnt)
        with self.assertRaises(RuntimeError):
            aln0=egglib.wrappers.muscle(dna, verbose=False)
        egglib.wrappers.paths['muscle'] = cache

        aln0=egglib.wrappers.muscle(dna, verbose=False)
        with self.assertRaises(TypeError):
            aln0=egglib.wrappers.muscle('dna', verbose=False)

        with self.assertRaises(TypeError):
            aln0=egglib.wrappers.muscle(dna, ref='error', verbose=False)

        with self.assertRaises(TypeError):
            egglib.wrappers.muscle(dna, ref=aln0, verbose=False)

        with self.assertRaises(ValueError):
            egglib.wrappers.muscle(dna, verbose=False, error='error')

        with self.assertRaises(ValueError):
            egglib.wrappers.muscle(dna, verbose=False, anchorspacing='error')

        with self.assertRaises(ValueError):
            egglib.wrappers.muscle(dna, verbose=False, cluster1='error')

    def test_alphabet(self):
        dna = egglib.io.from_fasta(os.path.join(path_T, 'cds.fas'), egglib.alphabets.DNA, labels=True)
        codons = egglib.io.from_fasta(os.path.join(path_T, 'cds.fas'), egglib.alphabets.DNA, labels=True)
        for i in codons:
            if i.ls%3!=0: i.sequence = i.sequence[:i.ls//3*3]
        codons.to_codons()
        prot = egglib.tools.translate(codons)
        codons = egglib.Container(alphabet=egglib.alphabets.codons)
        for sam in dna:
            seq = sam.sequence[:]
            if len(seq)%3:
                seq = list(seq)
                while len(seq)%3 != 0: del seq[-1]
                seq = ''.join(seq)
            codons.add_sample(sam.name, [seq[i:i+3] for i in range(0, len(seq), 3)])

        dna_a = egglib.wrappers.muscle(dna ,verbose=False, seqtype='dna')
        prot_a = egglib.wrappers.muscle(prot ,verbose=False, seqtype='protein')
        with self.assertRaises(ValueError):
            codons_a = egglib.wrappers.muscle(codons ,verbose=False, seqtype='codon')
        with self.assertRaises(ValueError):
            codons_a = egglib.wrappers.muscle(codons ,verbose=False, seqtype='dna')
        egglib.wrappers.muscle(dna_a, ref=dna_a)
        egglib.wrappers.muscle(prot_a, ref=prot_a)
        egglib.wrappers.muscle(dna_a, ref=dna_a, seqtype='dna')
        egglib.wrappers.muscle(prot_a, ref=prot_a, seqtype='protein')

        with self.assertRaises(ValueError):
            prot_a = egglib.wrappers.muscle(prot ,verbose=False, seqtype='dna')
        with self.assertRaises(ValueError):
            dna_a = egglib.wrappers.muscle(dna ,verbose=False, seqtype='protein')

        with self.assertRaises(ValueError):
            egglib.wrappers.muscle(dna_a, ref=prot_a)
        with self.assertRaises(ValueError):
            egglib.wrappers.muscle(prot_a, ref=dna_a)

        with self.assertRaises(ValueError):
            egglib.wrappers.muscle(dna_a, ref=prot_a, seqtype='dna')
        with self.assertRaises(ValueError):
            egglib.wrappers.muscle(prot_a, ref=dna_a, seqtype='dna')

        with self.assertRaises(ValueError):
            egglib.wrappers.muscle(prot_a, ref=dna_a, seqtype='protein')
        with self.assertRaises(ValueError):
            egglib.wrappers.muscle(dna_a, ref=prot_a, seqtype='protein')
