import os, egglib, sys, unittest, random, re, gc, time
from collections import Iterable
path = os.path.dirname(__file__)
path_T=os.path.join(path, 'correct_files')
path_F=os.path.join(path, 'erroneous_files')

class GFF3_test(unittest.TestCase):

    def setUp(self):
        fname='Populus_trichocarpa_short_thinned.gff3'
        self.gff3=egglib.io.GFF3(os.path.join(path_T,fname))

    def tearDown(self):
        del self.gff3

    def test_GFF3_T(self):
        self.assertIsInstance(self.gff3, egglib.io._gff3.GFF3)

    def test_num_top_features_T(self):
        ntf=self.gff3.num_top_features
        self.assertEqual(ntf, 16212)

    def test_num_tot_features_T(self):
        nttf=self.gff3.num_tot_features
        self.assertEqual(nttf, 22992)

    def test_feature_iter_GFF3_T(self):
        fname='Osativa_193_gene_thinned.gff3'
        gff3=egglib.io.GFF3(os.path.join(path_T,fname))
        f_iter=gff3.iter_features('Chr1', 1080000, 2510000)
        for feat in f_iter: 
            self.assertIsInstance(feat, egglib.io.Gff3Feature)
            self.assertEqual(feat.ID, 'LOC_Os01g02940')
            self.assertEqual(feat.attributes['Name'], 'LOC_Os01g02940')
            self.assertEqual(feat.source, 'phytozome8_0')
            break

    def test_mini_GFF3(self):
        A = egglib.io.GFF3.from_string(open(os.path.join(path_T, 'a.gff3')).read())
        B = egglib.io.GFF3(os.path.join(path_T, 'a.gff3'))
        C = egglib.io.GFF3(os.path.join(path_T, 'b.gff3'))

        self.assertEqual(A.version, '3')
        self.assertEqual(A.regions, {'1': (1-1, 500000-1)})
        self.assertEqual(A.feature_ontology, ['X001', 'X002'])
        self.assertEqual(A.attribute_ontology, ['X003'])
        self.assertEqual(A.source_ontology, ['X004', 'X005'])
        self.assertEqual(A.species, 'A species')
        self.assertEqual(A.genome_build, ('source', 'buildName'))
        self.assertEqual(A.sequences.fasta(), '>1\nAAAGCGCCGGGCGCGCCC\n')
        self.assertEqual(B.sequences.fasta(), '>1\nAAAGCGCCGGGCGCGCCC\n')
        self.assertEqual(C.sequences.fasta(), '>1\nAAAGCGCCGGGCGCGCCC\n>2\nTCCGCGCG\n')
        self.assertEqual(A.num_seqid, 2)
        self.assertEqual(A.list_seqid, ['1', 'chr3'])
        self.assertEqual(A.num_top_features, 6)
        self.assertEqual(A.num_tot_features, 24)

        it = [(i.seqid, i.start, i.end) for i in A]
        self.assertEqual(it, [('1', 295054, 303569), ('1', 494999, 549999), ('chr3', 0, 22), ('chr3', 27, 34), ('chr3', 56, 74), ('chr3', 87, 101)])

        it = [(i.seqid, i.start, i.end) for i in A.iter_features()]
        self.assertEqual(it, [('1', 295054, 303569), ('1', 494999, 549999), ('chr3', 0, 22), ('chr3', 27, 34), ('chr3', 56, 74), ('chr3', 87, 101)])

        it = [(i.seqid, i.start, i.end) for i in A.iter_features(seqid='1')]
        self.assertEqual(it, [('1', 295054, 303569), ('1', 494999, 549999)])

        it = [(i.seqid, i.start, i.end) for i in A.iter_features(seqid='1', start=295200, end=301000, all_features=True)]
        self.assertEqual(it, [('1', 295251, 295332), ('1', 295251, 295737), ('1', 297367, 297726), ('1', 298780, 298876), ('1', 299251, 299681), ('1', 300452, 300607)])

        it = [(i.seqid, i.start, i.end) for i in A.iter_features(seqid='chr3', start=25, end=100)]
        self.assertEqual(it, [('chr3', 27, 34), ('chr3', 56, 74)])

        [feat] = list(A.iter_features(seqid='1', start=298780, end=298876, all_features=True))

        self.assertEqual(feat.seqid, '1')
        self.assertEqual(feat.source, 'jgi')
        self.assertEqual(feat.type, 'exon')
        self.assertEqual(feat.start, 298780)
        self.assertEqual(feat.end, 298876)
        self.assertEqual(feat.score, None)
        self.assertEqual(feat.strand, '+')
        self.assertEqual(len(feat.segments), 1)
        self.assertEqual(feat.segments[0], (298780, 298876, None))
        self.assertEqual(len(feat.all_parts), 1)
        self.assertEqual(len(feat.descendants), 0)
        self.assertEqual(len(feat.parents), 1)
        self.assertEqual(feat.parents[0].ID, 'transcript:POPTR_0001s00390.2')
        dest = []
        feat._ultimate_parents(dest)
        self.assertEqual(len(dest), 1)
        self.assertEqual(dest[0].ID, 'gene:POPTR_0001s00390')
        ref = {
             'Parent': ('transcript:POPTR_0001s00390.2',),
             'Name': 'POPTR_0001s00390.2.exon4',
             'constitutive': '1',
             'ensembl_end_phase': '1',
             'ensembl_phase': '0',
             'exon_id': 'POPTR_0001s00390.2.exon4',
             'rank': '4',
             'version': '1',
             'ID': None,
             'Alias': None,
             'Target': None,
             'Gap': None,
             'Derives_from': None,
             'Note': None,
             'Dbxref': None,
             'Ontology_term': None,
             'Is_circular': False}
        self.assertEqual(feat.attributes, ref)

    def test_CDS_feat(self):
        gff3 = egglib.io.GFF3.from_string(open(os.path.join(path_T, 'a.gff3')).read())

        for feat in gff3.iter_features(all_features=True):
            feat.seqid, type(feat.start), feat.end, feat.type

        feats = list(gff3.iter_features(seqid='1', start=295333, end=301972, all_features=True))
        cds =  []
        for feat in feats:
            if feat.type == 'CDS': cds.append(feat)
        self.assertEqual(len(cds), 1)
        cds = cds[0]
        for a, b, c in cds.segments: self.assertIsInstance(c, int)

    def test_feat_count(self):
        fname = os.path.join(path_T, 'Populus_trichocarpa_short_thinned.gff3')
        gff = egglib.io.GFF3(fname)
        types = {}
        for seqid in '12':
            for feat in gff.iter_features(seqid, 0, 100000000000000):
                if feat.type not in types: types[feat.type] = 0
                types[feat.type] += 1
        ctrl = {}
        f = open(fname)
        for line in f:
            if line[0] != '#':
                bits = line.split('\t')
                assert len(bits) == 9
                tp = bits[2]
                attrs = bits[8]
                P = None
                for attr in attrs.split(';'):
                    k, v = attr.split('=')
                    if k == 'Parent':
                        assert P is None
                        P = v
                if P is None:
                    if tp not in ctrl: ctrl[tp] = 0
                    ctrl[tp] += 1
        self.assertDictEqual(types, ctrl)

class GFF3Feature_test(unittest.TestCase):
    def setUp(self):
        fname='Osativa_193_gene_thinned.gff3'
        self.gff3=egglib.io.GFF3(os.path.join(path_T,fname))
        self.f_iter=self.gff3.iter_features('Chr1', 1080000, 2510000)

    def tearDown(self):
        del self.gff3

    def test_GFF3Feature_T(self):
        for feat in self.f_iter: 
            self.assertIsInstance(feat, egglib.io.Gff3Feature)
        
    def test_GFF3Feature_property_T(self):
        for feat in self.f_iter: 
            self.assertEqual(feat.attributes, {'ID': 'LOC_Os01g02940', 'Name': 'LOC_Os01g02940',
                'Alias': None, 'Parent': None, 'Target': None,
                'Gap': None, 'Derives_from': None, 'Note': None,
                'Dbxref': None, 'Ontology_term': None,
                'Is_circular': False})
            self.assertEqual(feat.start, 1089742)
            self.assertEqual(feat.end, 1093527)
            self.assertEqual(feat.seqid, 'Chr1')
            self.assertEqual(feat.type, 'gene')
            self.assertEqual(feat.score, None)
            self.assertEqual(feat.strand, '-')
            self.assertEqual(feat.ID, 'LOC_Os01g02940')
            self.assertEqual(feat.source, 'phytozome8_0')
            self.assertEqual(len(feat.segments), 1)
            self.assertEqual(feat.segments, [(1089742, 1093527, None)])
            self.assertEqual(feat.parents, [])
            self.assertEqual(len(feat.descendants), 5)
            self.assertEqual(len(feat.all_parts), 49)
            break

    def test_get_part_T(self):
        for feat in self.f_iter: 
            self.assertIsInstance(feat.descendants[0], egglib.io.Gff3Feature)

    def test_get_part_E(self):
        for feat in self.f_iter: 
            with self.assertRaises(IndexError):
                feat.descendants[10]

    def test_get_parent_E(self):
        for feat in self.f_iter: 
            with self.assertRaises(IndexError):
                feat.parents[10]
