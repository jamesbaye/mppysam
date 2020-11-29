from collections import namedtuple

Region = namedtuple("Region", ["contig", "start", "stop"])

def region_length(region):
    return region.stop - region.start

def chunk_regions(regions, chunks, chunkby):
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
    elif chunkby == "gtf":
        ## First compute "contig" region boundaries.
        ##   Take gtf. if no features exist at boundary, take that boundary. else,
        ##   take closest boundary value where no features exist.
        raise NotImplementedError
    else:
        raise NotImplementedError

def chunk_region(region, chunks):
    target_chunksize = region_length(region) / chunks
    contig, start, stop = region
    chunk_start = start
    chunk_stop = start + target_chunksize
    for _ in range(chunks):
        yield Region(contig, round(chunk_start), round(chunk_stop))
        chunk_start = chunk_stop
        chunk_stop += target_chunksize
