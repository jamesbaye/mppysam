import pysam
import mppysam.regions as rg

def open_pysam(filepath_or_object, mode="rb"):
    return pysam.AlignmentFile(filepath_or_object, mode)

def segment_to_dict(segment):
    """Wrapper for pysam.AlignedSegment.to_dict()"""
    return segment.to_dict()

def get_all_regions(bamfilepath):
    with open_pysam(bamfilepath, "rb") as samfile:
        contigs = samfile.references
        lens = samfile.lengths
    return [rg.Region(contig, 0, int(end)) for contig, end in zip(contigs, lens)]

def fetch_rows(bamfilepath, region, row_func):
    contig, start, stop = region
    reads = []
    with open_pysam(bamfilepath, "rb") as samfile:
        reads = [row_func(read) for read in samfile.fetch(contig, start, stop)]
    return reads
