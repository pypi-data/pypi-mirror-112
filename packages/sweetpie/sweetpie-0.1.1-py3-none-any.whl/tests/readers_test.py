import unittest

from sweetpie.readers import CoNLLFileReader


class ReadersTest(unittest.TestCase):

    def test_conll_file_reader(self):
        reader = CoNLLFileReader()
        features, labels = reader.read('data/cpd-20210115.train')
        print(f'\nsize of features: {len(features)}, size of labels: {len(labels)}')
        print(features[:2])
        print(labels[:2])


if __name__ == "__main__":
    unittest.main()
