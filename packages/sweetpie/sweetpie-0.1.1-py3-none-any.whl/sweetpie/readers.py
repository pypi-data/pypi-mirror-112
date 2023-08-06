import abc
import logging
import os


class AbstractFileReader(abc.ABC):

    @abc.abstractmethod
    def read(self, files, **kwargs):
        raise NotImplementedError()


class CoNLLFileReader(AbstractFileReader):

    def __init__(self, sep='\t', feature_index=0, label_index=1, **kwargs):
        super().__init__()
        self.findex = feature_index
        self.lindex = label_index
        self.sep = sep

    def read(self, conll_files, **kwargs):
        features, labels = [], []

        def _collect_callback(feature, label):
            features.append(feature)
            labels.append(label)

        self._read(conll_files, callback=_collect_callback)
        return features, labels

    def _read(self, input_files, callback, **kwargs):
        if isinstance(input_files, str):
            input_files = [input_files]
        for f in input_files:
            if not os.path.exists(f):
                logging.warning('File %s doen not exist.', f)
                continue
            with open(f, mode='rt', encoding='utf8') as fin:
                feature, label = [], []
                for line in fin:
                    parts = line.rstrip('\n').split(self.sep)
                    if len(parts) >= 2:
                        feature.append(parts[self.findex].strip())
                        label.append(parts[self.lindex].strip())
                        continue
                    if callback:
                        callback(feature, label)
                    feature, label = [], []
            logging.info('Finished to read file: %s', f)
        logging.info('Finished to read all files.')
