import pandas as pd
import mppysam.multiproc as mpp
import mppysam.pysam_helper as ph


def read_bam(bamfilepath, contigs=None, starts=None, ends=None,
             processes=None, timeout=None, chunks=None):
    kwargs_df = make_fetch_args(bamfilepath, contigs, starts, ends, chunks)
    res = mpp.apply(fetch, kwargs_df, processes=processes, timeout=timeout)
    return res

def fetch(bamfilepath, contig=None, start=None, end=None,
         read_func=lambda x: x.to_dict()):
    reads = []
    with ph.open_pysam(bamfilepath, "rb") as samfile:
        for read in samfile.fetch(contig, start, end):
            reads.append(read_func(read))
    return reads

def make_fetch_args(bamfilepath, contigs, starts, ends, chunks):
    if contigs is None:
        contigs = get_all_contigs(bamfilepath)
    if chunks is None or chunks < len(contigs):
        kwargs_df = pd.DataFrame({
            "bamfilepath": bamfilepath,
            "contig": contigs
        })
    else:
        # split contigs by len in order to get right number of chunks
        raise NotImplementedError
    return kwargs_df

def get_all_contigs(bamfilepath):
    with ph.open_pysam(bamfilepath, "rb") as samfile:
        contigs = samfile.references
    return contigs
