import multiprocessing as mp

def apply(func, args_list, processes=None, timeout=None):
    output = []
    with mp.Pool(processes=processes) as pool:
        results = []
        for args in args_list:
            results.append(pool.apply_async(func, args))
        output = [item for res in results for item in res.get(timeout=timeout)]
    return output
