from functools import partial
import mppysam.mp_helper as mpp
import mppysam.pysam_helper as ph
import mppysam.regions as rg

def read_bam(bamfilepath, row_func=None, regions=None,
        processes=None, timeout=None, chunkby="contig", chunks=None):
    """Read an indexed BAM file by row.

    Supports multiprocessing with flexible chunking strategies
    and fetching of rows only within specific genomic regions.

    Args:
        bamfilepath (str): Path to a BAM file.
        row_func (callable, optional): The function applied to each BAM row object.
            Must take a pysam.AlignedSegment as an argument.
            Defaults to returning all the row content as a dict
                (`pysam.AlignedSegment.to_dict`).
        regions (iterable, optional): An iterable of (contig, start, stop) regions
            to filter rows on. If None, all rows are read.
        processes (int, optional): The number of worker processes to use.
            Defaults to the number returned by `os.cpu_count()`.
        timeout (int, optional): Number of seconds each process has to return its
            work before a `multiprocessing.TimeoutError` is raised.
            If None, no timeout is enforced.
        chunkby:
        chunks:
    """
    row_func = ph.segment_to_dict if row_func is None else row_func
    return apply_bam(bamfilepath, row_func, regions,
        processes, timeout, chunkby, chunks
    )

def apply_bam(bamfilepath, row_func, regions=None,
        processes=None, timeout=None, chunkby=None, chunks=None):
    regions = ph.get_all_regions(bamfilepath) if regions is None else regions
    return mpp.apply(
        partial(ph.fetch_rows, bamfilepath, row_func=row_func),
        args_list = [(region,) for region in rg.chunk_regions(regions, chunks, chunkby)],
        processes=processes,
        timeout=timeout
    )
