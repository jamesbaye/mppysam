import unittest
import mppysam.read_bai as rbi

class TestReadBai(unittest.TestCase):
    """Test read_bai()."""
    
    @classmethod
    def setUpClass(cls):
        cls.bai = rbi.read_bai("./mppysam/tests/data/ex1_10k.bam.bai")
    
    def test_bai_magic_string_is_correct(self):
        self.assertEqual(self.bai.magic, b'BAI\x01')
    
    def test_bai_n_unmapped_is_correct(self):
        self.assertEqual(self.bai.n_no_coor, 0)
    
    def test_bai_n_references_is_correct(self):
        self.assertEqual(self.bai.n_ref, 352)
    
    def test_bai_refs_have_bins(self):
        for i, ref in enumerate(self.bai.refs):
            self.assertGreaterEqual(ref.n_bin, 0, f"ref #{i}")
    
    def test_bai_bins_have_chunks(self):
        for i, ref in enumerate(self.bai.refs):
            for refbin in ref.bins:
                self.assertGreater(refbin.n_chunk, 0, f"ref #{i}; bin #{refbin.i_bin}")
    
    def test_bai_chunks_are_ordered(self):
        for i, ref in enumerate(self.bai.refs):
            for j, refbin in enumerate(ref.bins):
                current_offset = -1
                for chunk_beg, chunk_end in refbin.chunks:
                    self.assertGreater(chunk_end, chunk_beg,
                        f"ref #{i}; bin #{refbin.i_bin}")
                    self.assertGreater(chunk_beg, current_offset)
                    current_offset = chunk_beg
    
    def test_bai_refs_have_intervals(self):
        for i, ref in enumerate(self.bai.refs):
            self.assertGreaterEqual(ref.n_intv, 0, f"ref #{i}")
    
    def test_bai_intervals_are_ordered(self):
        for i, ref in enumerate(self.bai.refs):
            current_offset = -1
            for j, intv in enumerate(ref.intvs):
                self.assertGreaterEqual(intv.ioffset, current_offset,
                    f"ref #{i}; intv #{j}")
                current_offset = intv.ioffset
    
