import unittest
import mppysam.mp_helper as mpp

def add(a=0, b=0):
    return (a + b, )

class TestApplyWithAdd(unittest.TestCase):
    """Test apply() with a simple add function."""

    def test_returns_empty_list_if_empty_args(self):
        args_list = []
        self.assertEqual(mpp.apply(add, args_list, processes=1), [])

    def test_returns_one_output_if_one_call(self):
        args_list = [(1, 2)]
        self.assertEqual(mpp.apply(add, args_list, processes=1), [3])
    
    def test_returns_multiple_outputs_if_multiple_calls(self):
        args_list = [(1, 2), (7, 0), (5, -1)]
        self.assertEqual(mpp.apply(add, args_list, processes=1), [3, 7, 4])
    
    def test_returns_multiple_outputs_if_multiple_calls_2_processes(self):
        args_list = [(1, 2), (7, 0), (5, -1)]
        self.assertEqual(mpp.apply(add, args_list, processes=2), [3, 7, 4])

if __name__ == "__main__":
    unittest.main()
