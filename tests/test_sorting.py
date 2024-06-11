
import unittest
from borg_sort import borg_sort

class TestBorgSort(unittest.TestCase):
    def test_sorting(self):
        data = [5, 3, 8, 4, 2, 7, 1, 10]
        sorted_data = borg_sort(data)
        self.assertEqual(sorted_data, sorted(data))

if __name__ == '__main__':
    unittest.main()
