from __future__ import print_function
from pysam.libcalignmentfile cimport AlignmentFile

cdef extern from "htslib/hts.h":
    ctypedef struct hts_idx_t:
        int fmt
    
    int hts_idx_get_n_no_coor(hts_idx_t* idx)
    int hts_idx_get_stat(hts_idx_t* idx, int tid, int* mapped, int* unmapped)

#cdef extern from "stdint.h":
#    ctypedef unsigned char uint8_t
#    ctypedef signed int int32_t
#    ctypedef unsigned int uint32_t
#    ctypedef signed long int64_t
#    ctypedef unsigned long long uint64_t

#ctypedef int64_t hts_pos_t

#ctypedef struct lidx_t:
#    hts_pos_t n, m
#    uint64_t *offset

##ctypedef khash_t(bin) bidx_t

#ctypedef struct hts_idx_t:
##    From pysam/htslib/hts.c l:1541
#    int fmt, min_shift, n_lvls, n_bins
#    uint32_t l_meta
#    int32_t n, m
#    uint64_t n_no_coor
##    bidx_t **bidx
#    lidx_t *lidx
#    uint8_t *meta # MUST have a terminating NUL on the end
#    int tbi_n, last_tbi_tid
##    struct {
##        uint32_t last_bin, save_bin;
##        hts_pos_t last_coor;
##        int last_tid, save_tid, finished;
##        uint64_t last_off, save_off;
##        uint64_t off_beg, off_end;
##        uint64_t n_mapped, n_unmapped;
##    } z; # keep internal states


def get_index(bamfilepath, tid=0):
    cdef AlignmentFile samfile = AlignmentFile(bamfilepath, "rb")
    
    # hts methods compile and work as expected
    print(hts_idx_get_n_no_coor(samfile.index))
    cdef int mapped, unmapped
    hts_idx_get_stat(samfile.index, tid, &mapped, &unmapped)
    print(mapped, unmapped)
    
    # direct access fails
    print(samfile.index.fmt)
    
#    cdef hts_idx_t *idx = samfile.index
#    print(idx.fmt, idx.min_shift, idx.n_lvls, idx.n_bins)
#    print(idx.l_meta)
#    print(idx.n, idx.m)
#    print(idx.n_no_coor)
#    print(idx.lidx.n, idx.lidx.m, idx.lidx.offset[0])
#    print(idx.lidx[1].n, idx.lidx[1].m, idx.lidx[1].offset[0])
#    print(idx.meta)
#    print(idx.tbi_n, idx.last_tbi_tid)

