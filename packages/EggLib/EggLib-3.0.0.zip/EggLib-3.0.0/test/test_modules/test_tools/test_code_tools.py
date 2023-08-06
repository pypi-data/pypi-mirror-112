import os, egglib, sys, unittest, random, re, gc, time
from collections import Iterable
path = os.path.dirname(__file__)
path_T=os.path.join(path, 'correct_files')
path_F=os.path.join(path, 'erroneous_files')

class Translator_test(unittest.TestCase):
    def test_translator_T(self):
        trans=egglib.tools.Translator(code=5)
        self.assertIsInstance(trans, egglib.tools._code_tools.Translator)

    def test_translator_E(self):
        with self.assertRaises(ValueError):
            trans=egglib.tools.Translator(code=50) #<-----

    def test_translate_codon_T(self):
        trans=egglib.tools.Translator(code=5)
        codon=trans.translate_codon('AGT')
        self.assertEqual(codon,'S') #<-----

    def test_translate_align_T(self):
        trans=egglib.tools.Translator(code=1)
        aln=egglib.Align(egglib.alphabets.DNA)
        aln.ng = 2
        aln.add_samples([('CDS1', 'ATGGACCCCCTTGGGGACACGCTGCGC', ['0','0']),
                 ('CDS2', 'GCGACTGCGGGAGGCCTTCCACGCGGA', ['0','0']),
                 ('CDS3', 'CCTGGTTCCGCTACTTCAACGCCGGCG', ['0','1']),
                 ('CDS4', 'TGCTGCCTGCCCTGCAGAGCACCATCT', ['0','1']),
                 ('CDS5', 'GAAGCTCAACGCCCTCCGCTACCCGCC', ['1','2'])])
        aln.to_codons()
        aln_prot=trans.translate_align(aln)
        self.assertIsInstance(aln_prot, egglib._interface.Align) #<-----

        prot_seq=['MDPLGDTLR','ATAGGLPRG','PGSATSTPA','CCLPCRAPS']
        for i in range(0,4):
            seq=aln_prot.get_sequence(i).string()
            self.assertEqual(seq, prot_seq[i])

        f_name='sequence.fa'
        aln2 = egglib.io.from_fasta(os.path.join(path_T,f_name), alphabet=egglib.alphabets.DNA, labels=False, cls=egglib._interface.Align)
        aln2.to_codons(frame=egglib.tools.ReadingFrame([(0, 11), (30, 63, 1)], keep_truncated=True))
        aln2_prot=trans.translate_align(aln2)
        prot_seq2=['IVDXEVPPSSRIFFP', 'FEDXLLTPNLPYLHP', 'MAAXS-PSPN--YFP', 'MGTXSSASSSSSLES', 'MAAXSTPSPSNSCFL', 'MAAXECPSSTPSILS', 'MTTX-SPSNDSSAFA', 'LEEXKCSVSFPFYLP', 'MAAXSSPSSSSAASA', 'FDEXKSLEAFPFSLD', 'LEDXPHIFPFAYEAS', '---X-----------', 'MSLXAVSLSLARAAN', 'AANXKRRDALLAYAR', 'MAAXEEPFIRDASGS', 'MDRXALPPLPMALGG', 'MTAXPAEASFGSLVA', 'MAAXNPSMSQDSYMP', 'PPSXKRRALLLRYHR', 'MATXGAAMYDMVVDS', 'MAAX-APSPQMQKIA', 'MDAXASAVSSLLLSP']
        for i in range(0,22):
            self.assertIn(aln2_prot.get_sequence(i).string(),prot_seq2) #<-----

    def test_translate_align_E(self):
        trans=egglib.tools.Translator(code=1)
        cnt=egglib.Container(egglib.alphabets.DNA)
        cnt.ng = 2
        cnt.add_samples([('CDS1', 'ATGGACCCCCTTGGGGACACGCTGCGC', ['0','0']),
                 ('CDS2', 'GCGACTGCGGGAGGCCTTCCACGCGGA', ['0','0']),
                 ('CDS3', 'CCTGGTTCCGCTACTTCAACGCCGGCG', ['0','1']),
                 ('CDS4', 'TGCTGCCTGCCCTGCAGAGCACCATCT', ['0','1']),
                 ('CDS5', 'GAAGCTCAACGCCCTCCGCTACCCGCC', ['1','2'])])
        cnt.to_codons()
        with self.assertRaises(TypeError):
            aln_prot=trans.translate_align(cnt)

    def test_translate_container_T(self):
        trans=egglib.tools.Translator(code=1)
        cnt=egglib.Container(egglib.alphabets.DNA)
        cnt.ng = 2
        cnt.add_samples([('CDS1', 'ATGGACCCCCTTGGGGACACGCTGCGC', ['0','0']),
                 ('CDS2', 'GCGACTGCGGGAGGCCTTCCACGCGGA', ['0','0']),
                 ('CDS3', 'CCTGGTTCCGCTACTTCAACGCCGGCG', ['0','1']),
                 ('CDS4', 'TGCTGCCTGCCCTGCAGAGCACCATCT', ['0','1']),
                 ('CDS5', 'GAAGCTCAACGCCCTCCGCTACCCGCC', ['1','2'])])
        cnt.to_codons()
        cnt_prot=trans.translate_container(cnt)
        self.assertIsInstance(cnt_prot, egglib._interface.Container) #<-----

        prot_seq=['MDPLGDTLR','ATAGGLPRG','PGSATSTPA','PGSATSTPA','CCLPCRAPS']
        for i in range(0,4):
            seq=cnt_prot.get_sequence(i).string()
            self.assertIn(seq,prot_seq)

        f_name='sequence.fa'
        cnt2 = egglib.io.from_fasta(os.path.join(path_T,f_name), alphabet=egglib.alphabets.DNA, labels=False, cls=egglib._interface.Container)
        cnt2.to_codons()
        cnt2_prot=trans.translate_container(cnt2)

        f_name='resultats_prot.txt'
        file_=open(os.path.join(path_T,f_name),'r').read()
        for i in range(0,23):
            seq=cnt2_prot.get_sequence(i).string()
            r=file_.find(seq)
            self.assertTrue(r >= 0) #<-----

    def test_translate_container_E(self):
        trans=egglib.tools.Translator(code=1)
        aln=egglib.Align(egglib.alphabets.DNA)
        aln.ng = 2
        aln.add_samples([('CDS1', 'ATGGACCCCCTTGGGGACACGCTGCGC', ['0','0']),
                 ('CDS2', 'GCGACTGCGGGAGGCCTTCCACGCGGA', ['0','0']),
                 ('CDS3', 'CCTGGTTCCGCTACTTCAACGCCGGCG', ['0','1']),
                 ('CDS4', 'TGCTGCCTGCCCTGCAGAGCACCATCT', ['0','1']),
                 ('CDS5', 'GAAGCTCAACGCCCTCCGCTACCCGCC', ['1','2'])])
        aln.to_codons()

        with self.assertRaises(TypeError):
            cnt_prot=trans.translate_container(aln) #<-----

    def test_translate_sequence_T(self):
        trans=egglib.tools.Translator(code=1)
        seq_nuc="ATGCAGCGATTGCTCTTTCCGCCGTTGAGGGCCTTGAAGGGGAGGTGGTGTCTTTGGCTGATGAATGAACTCCGAAGAGTCCCAAAATGA"
        seq_prot=trans.translate_sequence(seq_nuc)
        self.assertEqual(seq_prot, "MQRLLFPPLRALKGRWCLWLMNELRRVPK*") #<-----
        self.assertIsInstance(seq_prot, str) #<-----

        aln=egglib.Align(egglib.alphabets.DNA)
        aln.ng=2
        aln.add_samples([('CDS1', 'ATGGACCCCCTTGGGGACACGCTGCGC', ['0','0'])])
        aln.to_codons()
        seq_prot3=trans.translate_sequence(aln.get_sequence(0))
        self.assertEqual(seq_prot3, 'MDPLGDTLR') #<-----

    def test_translate_sequence_E(self):
        trans=egglib.tools.Translator(code=1)
        seq_nuc="ATGCAGCGATTGCTCTTTCCGCCGTTGAGGGCCTTGAAGGGGAGGTGGTGTCTTTGGCTGATGAATGAACTCCGAAGAGTCCCAAAATGA"
        with self.assertRaises(ValueError):
            seq_prot=trans.translate_sequence(seq_nuc, frame= egglib.tools.ReadingFrame([(0,11),(0, 800)])) #<-----

class BackalignError_test(unittest.TestCase):
    def test_name_T(self):
        translator= egglib.tools.Translator(code=1)
        cds = egglib.io.from_fasta(os.path.join(path_F, 'LYK.E2.cds'), alphabet=egglib.alphabets.DNA)
        prot_aln = egglib.io.from_fasta(os.path.join(path_T, 'LYK.prot.aln'), alphabet=egglib.alphabets.protein)
        ns=prot_aln.ns
        ls=prot_aln.ls
        nucl = cds._obj
        aln = prot_aln._obj
        names_i = [nucl.get_name(i) for i in range(ns)]

        B_error=egglib.tools.BackalignError(names_i[0], nucl.get_sample, aln.get_sample, 0, 0, ls, nucl.get_nsit_sample(0), translator)
        self.assertEqual(B_error.name,'VvLYK2') #<-----

    def test_alignment_T(self):
        translator= egglib.tools.Translator(code=1)
        cds = egglib.io.from_fasta(os.path.join(path_F, 'LYK.E2.cds'), alphabet=egglib.alphabets.DNA)
        prot_aln = egglib.io.from_fasta(os.path.join(path_T, 'LYK.prot.aln'), alphabet=egglib.alphabets.protein)
        ns=prot_aln.ns
        ls=prot_aln.ls
        nucl = cds._obj
        aln = prot_aln._obj
        names_i = [nucl.get_name(i) for i in range(ns)]
        B_error=egglib.tools.BackalignError(names_i[9], nucl.get_sample, aln.get_sample, 9, 9, ls, nucl.get_nsit_sample(0), translator)
        self.assertRegexpMatches(B_error.alignment, '[~,#,-]')

class Outclass_tools_test(unittest.TestCase):

    def test_translate_T(self):
        f_name='sequence.fa'
        aln = egglib.io.from_fasta(os.path.join(path_T,f_name), labels=False, cls=egglib._interface.Align, alphabet=egglib.alphabets.DNA)
        cnt = egglib.io.from_fasta(os.path.join(path_T,f_name), labels=False, cls=egglib._interface.Container, alphabet=egglib.alphabets.DNA)
        seq='ATGGACCCCCTTGGGGACACGCTGCGC'
        aln.to_codons()
        cnt.to_codons()
        aln_prot=egglib.tools.translate(aln, code=1, in_place=False)
        cnt_prot=egglib.tools.translate(cnt, code=1, in_place=False)
        seq_prot=egglib.tools.translate(seq, code=1, in_place=False)
        aln0_prot=egglib.tools.translate(aln.get_sequence(0), code=1, in_place=False)
        file_=open(os.path.join(path_T,'resultats_prot.txt'),'r').read()
        for i in range(0,4):
            seq_cnt=cnt_prot.get_sequence(i).string()
            seq_aln=aln_prot.get_sequence(i).string()
            r=file_.find(seq_cnt)
            r2=file_.find(seq_aln)
            self.assertTrue(r >= 0) #<-----
            self.assertTrue(r2 >= 0) #<-----
        self.assertEqual(seq_prot, "MDPLGDTLR") #<-----
        self.assertEqual(aln0_prot, aln_prot.get_sequence(0).string()) #<-----

    def test_translate_E(self):
        seq=1510
        with self.assertRaises(ValueError):
            seq_prot=egglib.tools.translate(seq, code=1, in_place=True) #<-----

    def test_orf_iter_T(self):
        #>ENSG00000000457|1|169818772|169819672|ENSP00000356744;ENSP00000356746;ENSP00000407993;ENSP00000356745
        sequence=("GCACCTCTACTGTTTGCTACAAGTGGCCAGCAGCCATTTTGGATTTGGGCGGAAATGAAA"
            "TTAAAACTGTGCTGTTAAAAGCCTAAAAATTCAAGTCAAGACAAACTTAAGCATTCGACC"
            "AACACATCTAGAAAGGGGGCATCTTCGTGGACTAACTAGACCACTGGGGCAGTGAGTGAA"
            "ACTCGGTATCGTCGCGGCGCCCACACTTAAGATGGCACCGGCCTGAGACTCAGCTGTGCG"
            "GCCTCTCTACCTCGGTTCCTGGTTAGTTGGCCTCATTGGTGGCGTCGGAGGGAGGAAGGT"
            "GGGCCTTCTGTCCCGTTTCCGGACCCGTCTCTATGGTGTAGGAGAAACCCGGCCCCCAGA"
            "AGATTGTGGGTGTAGTGGCCACAGCCTTACAGGCAGGCAGGGGTGGTTGGTGTCAACAGG"
            "GGGGCCAACAGGGTACCAGAGCCAAGACCCTCGGCCTCCTCCCCCGCCGCCTTCCTGCAG"
            "GTAACAGGGAGCCCTGCGCTGCGCCCCCAGTCCTTGCAGGACTGCGCCGTGGGGGAAGGG"
            "GCCGGGCGGGGAGGAGGCGGCGGGCGCGCGCCCCGCTCGCGGGTCTGCGCTCTGGGGCCC"
            "GCGCGGGAGCGAGCTCGGCGCGGCGCCGGCGGCCGGTTGAGCTGTGCTCTCAGCTTCGGA"
            "GCAGCCTCCCCTTGCTGATTGTGGGGCGCCCTGTAATCTGCGCTTCGCGGGCGGCCCCCG"
            "ACGGGTGAGGCGCCCGCGGCCAGAGCTCTCCAAGGCGGCCGCGGAGTCGGTCCTCGCAGG"
            "GAGGTGTGGAAGGTGAGGGGCCAGCGAAGCGAGAGCGGCGCCTCGGCCCTTCAGTGACCC"
            "CGCGGGGTCGCGGCAAGCAGGGCGAGGGTGCTCGGCTGGGCGGGTCACTGTCCCGGGGCG")

        ORFs = [] # code to generate the list of ORFs (slightly different algorithm than in EggLib)
        for fr in 1, 2, 3:
            i = fr-1
            orf = None
            while i+4 < len(sequence):
                aa = egglib.tools.translate(sequence[i:i+3], allow_alt=True)
                if orf is None and aa == 'M':
                    orf = i
                if orf is not None and aa == '*':
                    tr = egglib.tools.translate(sequence[orf:i+3])
                    assert tr.count('*') == 1
                    assert tr[-1] == '*'
                    ORFs.append((orf, i+3, len(tr)-1, fr))
                    orf = None
                i += 3
        rc = egglib.tools.rc(sequence)
        def cpos(i): return len(sequence) - i - 1
        for fr in -1, -2, -3:
            i = -fr-1
            orf = None
            while i+4 < len(sequence):
                aa = egglib.tools.translate(rc[i:i+3], allow_alt=True)
                if orf is None and aa == 'M':
                    orf = i
                if orf is not None and aa == '*':
                    tr = egglib.tools.translate(rc[orf:i+3])
                    assert tr.count('*') == 1
                    assert tr[-1] == '*'
                    ORFs.append((cpos(i+2), cpos(orf)+1, len(tr)-1, fr))
                    orf = None
                i += 3

        orf=egglib.tools.orf_iter(sequence,  code=1, min_length=1, forward_only=False, force_start=True, allow_alt=True, force_stop=True)
        self.assertIsInstance(orf, Iterable)
        for i in orf:
            self.assertIn(i, ORFs)

    def test_orf_iter_E(self):
        sequence=("GCACCTCTACTGTTTGCTACAAGTGGCCAGCAGCCATTTTGGATTTGGGCGGAAATGAAA"
              "TTAAAACTGTGCTGTTAAAAGCCTAAAAATTCAAGTCAAGACAAACTTAAGCATTCGACC")
        with self.assertRaises(ValueError):
            orf = egglib.tools.orf_iter(sequence, code=10000)
        with self.assertRaises(ValueError):
            orf2 = egglib.tools.orf_iter(sequence, code=1, min_length=-10)

    def test_longest_orf_T(self):
        #>ENSG00000000457|1|169818772|169819672|ENSP00000356744;ENSP00000356746;ENSP00000407993;ENSP00000356745
        sequence=("GCACCTCTACTGTTTGCTACAAGTGGCCAGCAGCCATTTTGGATTTGGGCGGAAATGAAA"
            "TTAAAACTGTGCTGTTAAAAGCCTAAAAATTCAAGTCAAGACAAACTTAAGCATTCGACC"
            "AACACATCTAGAAAGGGGGCATCTTCGTGGACTAACTAGACCACTGGGGCAGTGAGTGAA"
            "ACTCGGTATCGTCGCGGCGCCCACACTTAAGATGGCACCGGCCTGAGACTCAGCTGTGCG"
            "GCCTCTCTACCTCGGTTCCTGGTTAGTTGGCCTCATTGGTGGCGTCGGAGGGAGGAAGGT"
            "GGGCCTTCTGTCCCGTTTCCGGACCCGTCTCTATGGTGTAGGAGAAACCCGGCCCCCAGA"
            "AGATTGTGGGTGTAGTGGCCACAGCCTTACAGGCAGGCAGGGGTGGTTGGTGTCAACAGG"
            "GGGGCCAACAGGGTACCAGAGCCAAGACCCTCGGCCTCCTCCCCCGCCGCCTTCCTGCAG"
            "GTAACAGGGAGCCCTGCGCTGCGCCCCCAGTCCTTGCAGGACTGCGCCGTGGGGGAAGGG"
            "GCCGGGCGGGGAGGAGGCGGCGGGCGCGCGCCCCGCTCGCGGGTCTGCGCTCTGGGGCCC"
            "GCGCGGGAGCGAGCTCGGCGCGGCGCCGGCGGCCGGTTGAGCTGTGCTCTCAGCTTCGGA"
            "GCAGCCTCCCCTTGCTGATTGTGGGGCGCCCTGTAATCTGCGCTTCGCGGGCGGCCCCCG"
            "ACGGGTGAGGCGCCCGCGGCCAGAGCTCTCCAAGGCGGCCGCGGAGTCGGTCCTCGCAGG"
            "GAGGTGTGGAAGGTGAGGGGCCAGCGAAGCGAGAGCGGCGCCTCGGCCCTTCAGTGACCC"
            "CGCGGGGTCGCGGCAAGCAGGGCGAGGGTGCTCGGCTGGGCGGGTCACTGTCCCGGGGCG")
        orf_l = egglib.tools.longest_orf(sequence, code=1, min_length=1, forward_only=False, force_start=True, allow_alt=True, force_stop=True)
        self.assertEqual(orf_l, (330, 834, 167, -1))

    def test_backalign_T(self):
        cds = egglib.io.from_fasta(os.path.join(path_T, 'LYK.cds'), alphabet=egglib.alphabets.DNA)
        cds.to_codons()
        prot_aln1 = egglib.io.from_fasta(os.path.join(path_T, 'LYK.prot.aln'), alphabet=egglib.alphabets.protein)
        cds_aln = egglib.tools.backalign(cds, prot_aln1)
        self.assertIsInstance(cds_aln, egglib.Align)
        self.assertEqual(''.join(cds.get_sequence(0)[:]), ''.join(cds_aln.get_sequence(0)[:]).replace("-",""))

    def test_backalign_E(self):
        cds = egglib.io.from_fasta(os.path.join(path_T, 'LYK.cds'), alphabet=egglib.alphabets.DNA)
        prot_aln1 = egglib.io.from_fasta(os.path.join(path_F, 'LYK.prot.E.aln'), alphabet=egglib.alphabets.protein)
        with self.assertRaises(ValueError):
            cds_aln = egglib.tools.backalign(cds, prot_aln1)

        cds2 = egglib.io.from_fasta(os.path.join(path_F, 'LYK.E.cds'), alphabet=egglib.alphabets.DNA)
        prot_aln2 = egglib.io.from_fasta(os.path.join(path_T, 'LYK.prot.aln'), alphabet=egglib.alphabets.protein)
        with self.assertRaises(ValueError):
            cds_aln2 = egglib.tools.backalign(cds2, prot_aln2, ignore_names=False)
        with self.assertRaises(ValueError):
            cds_aln2 = egglib.tools.backalign(cds2, prot_aln2, ignore_names=True)

        cds3 = egglib.io.from_fasta(os.path.join(path_F, 'LYK.E2.cds'), alphabet=egglib.alphabets.DNA)
        prot_aln3 = egglib.io.from_fasta(os.path.join(path_T, 'LYK.prot.aln'), alphabet=egglib.alphabets.protein)
        with self.assertRaises(ValueError):
            cds_aln3 = egglib.tools.backalign(cds3, prot_aln3, ignore_names=False)
        with self.assertRaises(ValueError):
            cds_aln3 = egglib.tools.backalign(cds3, prot_aln3, ignore_names=True)

    def test_trailingstop_T(self):
        aln = egglib.io.from_fasta(os.path.join(path_T, 'align_generate.fsa'), labels=False, alphabet=egglib.alphabets.DNA)
        frame = egglib.tools.ReadingFrame([(0, 10),(50,70),(120,180),(240,270), (300, 360)])
        aln.to_codons(frame=frame)
        n1_stop=egglib.tools.trailing_stops(aln, action=0)
        n2_stop= egglib.tools.trailing_stops(aln, action=0)
        n3_stop= egglib.tools.trailing_stops(aln, action=0)
        n4_stop= egglib.tools.trailing_stops(aln, action=2, replacement='NNN')
        self.assertEqual(n1_stop, 7)
        self.assertEqual(n2_stop, 7)
        self.assertEqual(n3_stop, 7)
        self.assertEqual(n4_stop, 7)

    def test_trailingstop_E(self):
        aln = egglib.io.from_fasta(os.path.join(path_T, 'align_generate.fsa'), labels=False, alphabet=egglib.alphabets.DNA)
        cnt = egglib.io.from_fasta(os.path.join(path_T, 'align_generate.fsa'), labels=False, cls=egglib._interface.Container, alphabet=egglib.alphabets.DNA)
        frame = egglib.tools.ReadingFrame([(0, 10),(50,70),(120,180),(240,270), (300, 360)])
        with self.assertRaises(ValueError):
            n1_stop = egglib.tools.trailing_stops(aln, action=0)
        aln.to_codons(frame=frame)
        with self.assertRaises(ValueError):
            n2_stop = egglib.tools.trailing_stops(aln, action=0, code=1000)
        with self.assertRaises(TypeError):
            n3_stop = egglib.tools.trailing_stops(cnt, action=0) # include outgroup was used here
        with self.assertRaises(TypeError):
            n4_stop = egglib.tools.trailing_stops(aln, action=2, replacement=0)

    def test_iter_stops_T(self):
        aln = egglib.io.from_fasta(os.path.join(path_T, 'align_generate.fsa'), labels=False, alphabet=egglib.alphabets.DNA)
        frame = egglib.tools.ReadingFrame([(0, 10),(50,70),(120,180),(240,270), (300, 360)])
        aln.to_codons(frame=frame)
        l_stop=list(egglib.tools.iter_stops(aln))
        r_stop=[(1, 9), (1, 20), (1, 59), (2, 55), (3, 14), (3, 59), (4, 33), (4, 58), (4, 59), (5, 3), (5, 23), (6, 16), (6, 59), (7, 28), (7, 57), (7, 59), (8, 46), (8, 57), (8, 59), (9, 24), (9, 54), (9, 56), (9, 59)]
        self.assertEqual(l_stop, r_stop)

    def test_iter_stops_E(self):
        aln = egglib.io.from_fasta(os.path.join(path_T, 'align_generate.fsa'), labels=False, alphabet=egglib.alphabets.DNA)
        cnt = egglib.io.from_fasta(os.path.join(path_T, 'align_generate.fsa'), labels=False, cls=egglib._interface.Container, alphabet=egglib.alphabets.DNA)
        frame = egglib.tools.ReadingFrame([(0, 10),(50,70),(300, 360)])
        cnt1 = egglib.tools.to_codons(cnt)
        aln1 = egglib.tools.to_codons(aln)
        aln2 = egglib.tools.to_codons(aln, frame=frame)

        with self.assertRaises(ValueError):
            for i in egglib.tools.iter_stops(aln1, code=1000): pass

    def test_has_stop_T(self):
        aln = egglib.io.from_fasta(os.path.join(path_T, 'align_generate.fsa'), labels=False, alphabet=egglib.alphabets.DNA)
        aln1 = egglib.tools.to_codons(aln)
        self.assertTrue(egglib.tools.has_stop(aln1, code=1))
        frame = egglib.tools.ReadingFrame([(0, 10)])
        aln2 = egglib.tools.to_codons(aln, frame=frame)
        self.assertFalse(egglib.tools.has_stop(aln2, code=1))
