import unittest
from .sorting import clean_and_sort


class CleandAndSortTestCases(unittest.TestCase):

    def test_clean_input_ints(self):
        test_input = ['1000', '25', '32', '100', '1', '9', '-1']
        expected = ['-1', '1', '9', '25', '32', '100', '1000']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_clean_input_texts(self):
        test_input = ['zebra', 'turtle' 'apple', 'picnic', 'computer', 'derpasaurus']
        expected = ['apple', 'computer', 'derpasaurus', 'picnic', 'turtle', 'zebra']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_clean_input_mixed(self):
        test_input = ['20', 'cat', 'bird', '12', 'dog']
        expected = ['12', 'bird', 'cat', '20', 'dog']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_dirty_input_ints(self):
        test_input = ['1&0&0)0', '2}5', '3{2', '1*0*0', '*1&', '!@#9', '-1%^&']
        expected = ['-1', '1', '9', '25', '32', '100', '1000']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_dirty_input_texts(self):
        test_input = ['ze%br-a', 'tur!+tle' 'ap!&pl(e', 'pi&cni)c', 'comp(*&uter', 'de$%^rpa^saurus']
        expected = ['apple', 'computer', 'derpasaurus', 'picnic', 'turtle', 'zebra']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_dirty_input_mixed(self):
        test_input = ['2$#0', 'cat', 'bi?rd', '1!2', 'do@g']
        expected = ['12', 'bird', 'cat', '20', 'dog']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_empty_input(self):
        test_input = []
        expected = []
        self.assertEqual(clean_and_sort(test_input), expected)


if __name__ == '__main__':
    unittest.main()
