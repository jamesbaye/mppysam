import pysam

def open_pysam(filepath_or_object, mode="rb"):
    return pysam.AlignmentFile(filepath_or_object, mode)
