import struct
from collections import namedtuple
from os.path import splitext

Idx = namedtuple("idx", ["magic", "n_ref", "refs", "n_no_coor"])
Ref = namedtuple("ref", ["n_bin", "bins", "n_intv", "intvs"])
Bin = namedtuple("bin", ["i_bin", "n_chunk", "chunks"])
Chunk = namedtuple("chunk", ["chunk_beg", "chunk_end"])
Intv = namedtuple("interval", ["ioffset"])

def bai_path(bamfilepath):
    """Return the path to BAI file in the same directory as BAM file."""
    return f"{bamfilepath}.bai"

def read_bai(baifilepath):
    """Read BAI index file.
    
    See https://samtools.github.io/hts-specs/SAMv1.pdf section 5.2.
    
    Args:
        baifilepath (str): Path to BAI file.
    Returns:
        A Idx namedtuple containing the parsed BAI data.
    """
    METADATA_IBIN = 37450 # pseudo-bin containing per-reference metadata. ignored.
    with open(baifilepath, "rb") as f:
        magic, n_ref = struct.unpack("4s i", f.read(4 + 4))
        refs = []
        for _ in range(n_ref):
            n_bin, = struct.unpack("i", f.read(4))
            bins = []
            for _ in range(n_bin):
                i_bin, n_chunk = struct.unpack("I i", f.read(4 + 4))
                chunks = []
                for _ in range(n_chunk):
                    chunk_beg, chunk_end = struct.unpack("Q Q", f.read(8 + 8))
                    chunks.append(Chunk(chunk_beg, chunk_end))
                if i_bin != METADATA_IBIN:
                    bins.append(Bin(i_bin, n_chunk, chunks))
            n_intv, = struct.unpack("i", f.read(4))
            intvs = []
            for _ in range(n_intv):
                ioffset, = struct.unpack("Q", f.read(8))
                intvs.append(Intv(ioffset))
            refs.append(Ref(n_bin, bins, n_intv, intvs))
        n_no_coor, = struct.unpack("Q", f.read(8))
        return Idx(magic, n_ref, refs, n_no_coor)
