import multiprocessing as mp

def apply(func, args_df, processes=None, timeout=None):
    output = []
    with mp.Pool(processes=processes) as pool:
        results = []
        for i in range(len(args_df.index)):
            results.append(pool.apply_async(func, args_df.iloc[i,]))
        output = [res.get(timeout=timeout) for res in results]
    return output
