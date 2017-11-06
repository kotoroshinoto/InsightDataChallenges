from typing import List
import unittest
from collections import deque
import click


def sort_words(words: 'List[str]'):
    # save "type" at each position into a list
    # split ints and texts into separate lists, sort independently
    # reconstruct output list using the types at each position to pull from the sorted lists
    strtypes = []
    ints = []
    texts = []
    answer = []
    for word in words:
        if word[0] == '-' or word.isdigit():
            strtypes.append(True)
            ints.append(word)
        else:
            strtypes.append(False)
            texts.append(word)
    ints = deque(sorted(ints, key=lambda x: int(x)))
    texts = deque(sorted(texts))
    for stype in strtypes:
        if stype:
            answer.append(ints.popleft())
        else:
            answer.append(texts.popleft())
    return answer


def clean_word(word: 'str'):
    #go char-by-char and remove text that isn't either alpha or numeric
    #make allowance for a single minus sign on left side of ints
    #rule for identifying an int: after all dirty content is removed, only digits remain
    minus_before_digit = False
    saw_digit = False
    w = ''
    for c in word:
        if c == '-' and not saw_digit:
            minus_before_digit = True
        digit=c.isdigit()
        alpha=c.isalpha()
        if not (digit or alpha):
            continue
        else:
            if digit:
                saw_digit = True
            w += c
    if w.isdigit() and minus_before_digit:
        return '-' + w
    else:
        return w


def clean_words(words: 'List'):
    cleaned = []
    for word in words:
        cleaned.append(clean_word(word))
    return cleaned


def clean_and_sort(words: 'List'):
    cleaned = clean_words(words)
    return sort_words(cleaned)


class CleaningTestCases(unittest.TestCase):
    def test_word_clean_text(self):
        word = '---!@a#$p%^p&*l()_e+*/'
        expected = 'apple'
        self.assertEqual(clean_word(word), expected)

    def test_word_clean_int_positive(self):
        word = '!@#1$%^0&*0()_0+*/'
        expected = '1000'
        self.assertEqual(clean_word(word), expected)

    def test_word_clean_int_negative(self):
        word = '---!-@-#1$0%0^0&*()_+*/'
        expected = '-1000'
        self.assertEqual(clean_word(word), expected)


class CleanAndSortTestCasesCLEAN(unittest.TestCase):
    def test_clean_input_ints(self):
        test_input = ['1000', '25', '32', '100', '1', '9', '-1']
        expected = ['-1', '1', '9', '25', '32', '100', '1000']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_clean_input_texts(self):
        test_input = ['zebra', 'turtle', 'apple', 'picnic', 'computer', 'derpasaurus']
        expected = ['apple', 'computer', 'derpasaurus', 'picnic', 'turtle', 'zebra']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_clean_input_mixed(self):
        test_input = ['20', 'cat', 'bird', '12', 'dog']
        expected = ['12', 'bird', 'cat', '20', 'dog']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_one_clean_item_text(self):
        test_input = ['derpasaurus']
        expected = ['derpasaurus']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_one_clean_item_int(self):
        test_input = ['20']
        expected = ['20']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_one_clean_negative_item_int(self):
        test_input = ['-20']
        expected = ['-20']
        self.assertEqual(clean_and_sort(test_input), expected)


class CleanAndSortTestCasesDIRTY(unittest.TestCase):
    def test_dirty_input_ints(self):
        test_input = ['1&0&0)0', '2}5', '3{2', '1*0*0', '*1&', '!@#9', '-1%^&']
        expected = ['-1', '1', '9', '25', '32', '100', '1000']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_dirty_input_texts(self):
        test_input = ['ze%br-a', 'tur!+tle', 'ap!&pl(e', 'pi&cni)c', 'comp(*&uter', 'de$%^rpa^saurus']
        expected = ['apple', 'computer', 'derpasaurus', 'picnic', 'turtle', 'zebra']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_dirty_input_mixed(self):
        test_input = ['2$#0', 'cat', 'bi?rd', '1!2', 'do@g']
        expected = ['12', 'bird', 'cat', '20', 'dog']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_one_dirty_item_text(self):
        test_input = ['de$%^rpa^saurus']
        expected = ['derpasaurus']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_one_dirty_item_int(self):
        test_input = ['2$#0']
        expected = ['20']
        self.assertEqual(clean_and_sort(test_input), expected)

    def test_one_dirty_negative_item_int(self):
        test_input = ['--2$#0']
        expected = ['-20']
        self.assertEqual(clean_and_sort(test_input), expected)


class CleanAndSortTestCasesEMPTY(unittest.TestCase):

    def test_empty_input(self):
        test_input = []
        expected = []
        self.assertEqual(clean_and_sort(test_input), expected)


@click.command()
@click.option('--test/--no-test', default=False, help='run unit tests')
@click.argument('inpath', type=click.Path(file_okay=True, dir_okay=False, readable=True, resolve_path=True), default='list.txt')
@click.argument('outpath', type=click.Path(file_okay=True, dir_okay=False, writable=True, resolve_path=True), default='result.txt')
def cli(inpath, outpath, test):
    if test:
        unittest.main(argv=['ignore me'], verbosity=2)
    with open(inpath, 'r') as infile:
        line = next(infile).rstrip()
        words = line.split()
        cleaned_and_sorted_words = clean_and_sort(words)
        with open(outpath, 'w') as outfile:
            print(" ".join(cleaned_and_sorted_words), file=outfile)


if __name__ == '__main__':
    cli()
