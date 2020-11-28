import unittest
import pandas as pd
import mppysam.mp_helper as mpp

def add(a=0, b=0):
    return a + b

class TestApplyWithAdd(unittest.TestCase):

    def test_returns_empty_list_if_empty_args(self):
        args_df = pd.DataFrame()
        self.assertEqual(mpp.apply(add, args_df, processes=1), [])

    def test_returns_one_output_if_one_call(self):
        args_df = pd.DataFrame({"a": [1], "b": [2]})
        self.assertEqual(mpp.apply(add, args_df, processes=1), [3])
    
    def test_returns_multiple_outputs_if_multiple_calls(self):
        args_df = pd.DataFrame({"a": [1, 7, 5], "b": [2, 0, -1]})
        self.assertEqual(mpp.apply(add, args_df, processes=1), [3, 7, 4])
    
    def test_returns_multiple_outputs_if_multiple_calls_2_processes(self):
        args_df = pd.DataFrame({"a": [1, 7, 5], "b": [2, 0, -1]})
        self.assertEqual(mpp.apply(add, args_df, processes=2), [3, 7, 4])

if __name__ == "__main__":
    unittest.main()
