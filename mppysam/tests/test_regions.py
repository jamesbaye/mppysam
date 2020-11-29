import unittest
import mppysam.regions as rg

class TestChunkRegions(unittest.TestCase):
    """Test chunk_regions()."""
    
    def test_does_not_chunk_if_more_regions_than_desired_chunks(self):
        regions = [rg.Region("chr1", 0, 1)]
        self.assertEqual(rg.chunk_regions(regions, 1, chunkby="contig"), regions)
        
        regions = [
            rg.Region("chr1", 0, 1), rg.Region("chr2", 20, 39), rg.Region("chr2", 5, 9)]
        self.assertEqual(rg.chunk_regions(regions, 2, chunkby="contig"), regions)

    def test_chunks_if_one_region_two_chunks(self):
        regions = [rg.Region("chr1", 0, 2)]
        self.assertEqual(
            rg.chunk_regions(regions, 2, chunkby="contig"),
            [rg.Region("chr1", 0, 1), rg.Region("chr1", 1, 2)]
        )
        
        regions = [rg.Region("chr1", 9, 12)]
        self.assertEqual(
            rg.chunk_regions(regions, 2, chunkby="contig"),
            [rg.Region("chr1", 9, 10), rg.Region("chr1", 10, 12)]
        )
    
    def test_chunks_if_one_region_three_chunks(self):
        regions = [rg.Region("chr1", 0, 3)]
        self.assertEqual(
            rg.chunk_regions(regions, 3, chunkby="contig"),
            [rg.Region("chr1", 0, 1), rg.Region("chr1", 1, 2), rg.Region("chr1", 2, 3)]
        )
        
        regions = [rg.Region("chr1", 9, 14)]
        self.assertEqual(
            rg.chunk_regions(regions, 3, chunkby="contig"),
            [
                rg.Region("chr1", 9, 11),
                rg.Region("chr1", 11, 12),
                rg.Region("chr1", 12, 14)
            ]
        )
    
    def test_chunks_if_two_regions_four_chunks(self):
        regions = [rg.Region("chr1", 0, 2), rg.Region("chr1", 10, 20)]
        self.assertEqual(
            rg.chunk_regions(regions, 4, chunkby="contig"),
            [
                rg.Region("chr1", 0, 2),
                rg.Region("chr1", 10, 13),
                rg.Region("chr1", 13, 17),
                rg.Region("chr1", 17, 20),
            ]
        )
