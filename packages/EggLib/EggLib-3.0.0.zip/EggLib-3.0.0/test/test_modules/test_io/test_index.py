import os, egglib, sys, unittest, random, re, gc, time
from collections import Iterable
path = os.path.dirname(__file__)
path_T=os.path.join(path, 'correct_files')

class  VcfIndex_test(unittest.TestCase):
    def test_object_aln_T(self):
        idx = egglib._eggwrapper.VcfIndex()
        self.assertIsInstance(idx, egglib._eggwrapper.VcfIndex)


if __name__ == '__main__':
    unittest.main()
