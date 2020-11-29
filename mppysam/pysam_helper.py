import pysam
from collections import namedtuple

def open_pysam(filepath_or_object, mode="rb"):
    return pysam.AlignmentFile(filepath_or_object, mode)

def segment_to_dict(segment):
    """Wrapper for pysam.AlignedSegment.to_dict()"""
    return segment.to_dict()

def get_all_contigs(bamfilepath):
    with open_pysam(bamfilepath, "rb") as samfile:
        contigs = samfile.references
    return contigs

Region = namedtuple("Region", ["contig", "start", "stop"])

def fetch_rows(bamfilepath, region, row_func):
    contig, start, stop = region
    reads = []
    with open_pysam(bamfilepath, "rb") as samfile:
        reads = [row_func(read) for read in samfile.fetch(contig, start, stop)]
    return reads
