from collections import namedtuple

Region = namedtuple("Region", ["contig", "start", "stop"])

def region_length(region):
    return region.stop - region.start

def chunk_regions(regions, chunks, chunkby, gtf=None):
    """Chunk regions by read count or contig length.
    
    Args:
        regions (iterable): An iterable of Region objects.
        chunks (int): A number of desired chunks.
        chunkby (str): Chunking policy. Either "contig" or "index".
            "contig" returns regions of similar contig length.
            "index" returns regions of similar read count.
        gtf (str, optional): A GTF file. If provided, constrains chunking such
            that a feature in GTF is never split between two or more regions.
    """
    if chunkby == "contig":
        if chunks is None or chunks <= len(regions):
            return regions
        else:
            target_chunksize = sum(region_length(region) for region in regions) / chunks
            chunks_per_regions = [
                max(1, round(region_length(region) / target_chunksize)) 
                for region in regions
            ]
            regions = [
                region_chunked
                for region, chunks_per_region in zip(regions, chunks_per_regions)
                for region_chunked in chunk_region(region, chunks_per_region)
            ]
            return regions
    elif chunkby == "index":
        raise NotImplementedError
    elif chunkby == "gtf":
        ## First compute "contig" region boundaries.
        ##   Take gtf. if no features exist at boundary, take that boundary. else,
        ##   take closest boundary value where no features exist.
        raise NotImplementedError
    else:
        raise NotImplementedError

def chunk_region(region, chunks):
    target_chunksize = region_length(region) / chunks
    contig, start, _ = region
    chunk_start = start
    for _ in range(chunks):
        yield Region(contig, round(chunk_start), round(chunk_start + target_chunksize))
        chunk_start += target_chunksize
