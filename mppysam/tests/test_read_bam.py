import unittest
import pysam
from unittest.mock import patch
import mppysam.read_bam as rb

def open_empty_pysam(*args, **kwargs):
    return MockPysamAlignmentFile()

def open_oneLine_pysam(*args, **kwargs):
    return MockPysamAlignmentFile(
        reads=[{
            "name": "ABC_123",
            "flag": "0",
            "ref_name": "1",
            "ref_pos": "10",
            "map_quality": "255",
            "cigar": "4S2M",
            "next_ref_name": "*",
            "next_ref_pos": "0",
            "length": "0",
            "seq": "ACTAGC",
            "qual": "FF,FF:",
            "tags": []
        }],
        header=pysam.AlignmentHeader.from_references(
            reference_names=["1"],
            reference_lengths=[100]
        )
        
    )

def open_multiLine_pysam(*args, **kwargs):
    return MockPysamAlignmentFile(
        reads=[
            {
                "name": "read1",
                "flag": "0",
                "ref_name": "1",
                "ref_pos": "10",
                "map_quality": "255",
                "cigar": "4S2M",
                "next_ref_name": "*",
                "next_ref_pos": "0",
                "length": "0",
                "seq": "ACTAGC",
                "qual": "FF,FF:",
                "tags": []
            },
            {
                "name": "read2",
                "flag": "16",
                "ref_name": "2",
                "ref_pos": "1000",
                "map_quality": "255",
                "cigar": "6M",
                "next_ref_name": "*",
                "next_ref_pos": "0",
                "length": "0",
                "seq": "CCTGAC",
                "qual": ":F,,F:",
                "tags": []
            },
            {
                "name": "read3",
                "flag": "1",
                "ref_name": "1",
                "ref_pos": "100",
                "map_quality": "255",
                "cigar": "6M",
                "next_ref_name": "*",
                "next_ref_pos": "0",
                "length": "0",
                "seq": "GCTAGC",
                "qual": "FFFFFF",
                "tags": []
            },
        ],
        header=pysam.AlignmentHeader.from_references(
            reference_names=["1", "2"],
            reference_lengths=[9999, 9999]
        )
        
    )

class MockPysamAlignmentFile:
    def __init__(self, reads=None, header=None):
        self.reads = [] if reads is None else reads
        self.header = pysam.AlignmentHeader() if header is None else header
        self.references = self.header.references
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        pass
    
    def fetch(self, contig, start, stop):
        return [
            pysam.AlignedSegment().from_dict(read, self.header)
            for read in self.reads
            if (
                contig is None
                or (
                    read["ref_name"] == contig
                    and (start is None or int(read["ref_pos"]) >= start)
                    and (stop is None or int(read["ref_pos"]) <= stop)
                )
            )
        ]
        

class TestReadBam(unittest.TestCase):
    """Test read_bam()."""
    maxDiff=None
    
    @patch("mppysam.pysam_helper.open_pysam", open_empty_pysam)
    def test_empty_open(self):
        self.assertEqual(rb.read_bam("mock_empty_filepath", processes=1), [])
    
    @patch("mppysam.pysam_helper.open_pysam", open_oneLine_pysam)
    def test_oneLine_open(self):
        self.assertCountEqual(
            rb.read_bam("mock_oneLine_filepath", processes=1),
            open_oneLine_pysam().reads
        )
    
    @patch("mppysam.pysam_helper.open_pysam", open_multiLine_pysam)
    def test_multiLine_open(self):
        self.assertCountEqual(
            rb.read_bam("mock_multiLine_filepath", processes=1),
            open_multiLine_pysam().reads
        )
    
    def test_bam_open_one_process(self):
        bam = rb.read_bam("./mppysam/tests/data/ex1_10k.bam", processes=1)
        self.assertEqual(
            bam[0]["name"],
            "A00489:517:HMJTNDRXX:2:1261:18557:24831_AGACTC_CTTGTAATAT"
        )
    
    def test_bam_open_two_processes(self):
        bam = rb.read_bam("./mppysam/tests/data/ex1_10k.bam", processes=2)
        self.assertEqual(
            bam[0]["name"],
            "A00489:517:HMJTNDRXX:2:1261:18557:24831_AGACTC_CTTGTAATAT"
        )
    
