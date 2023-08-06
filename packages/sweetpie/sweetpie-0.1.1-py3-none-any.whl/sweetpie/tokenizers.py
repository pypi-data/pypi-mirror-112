import abc
import os
from collections import namedtuple

TokenizerEncoding = namedtuple("TokenizerEncoding", ["text", "tokens", "ids", "type_ids", "attention_mask", "offsets"])


class AbstractTokenizer(abc.ABC):

    def encode(self, *args, **kwargs):
        raise NotImplementedError()

    def decode(self, *args, **kwargs):
        raise NotImplementedError()


class ChineseBertCharTokenizer(AbstractTokenizer):

    def __init__(self, bert_vocab_file, do_lower_case=True):
        super().__init__()
        self.vocab_file = bert_vocab_file
        self.token2id = self._load_bert_vocab(bert_vocab_file)
        self.id2token = {v: k for k, v in self.token2id.items()}
        self.unk_token = '[UNK]'
        self.pad_token = '[PAD]'
        self.cls_token = '[CLS]'
        self.sep_token = '[SEP]'
        self.mask_token = '[MASK]'
        self.unk_id = self.token2id[self.unk_token]
        self.pad_id = self.token2id[self.pad_token]
        self.cls_id = self.token2id[self.cls_token]
        self.sep_id = self.token2id[self.sep_token]
        self.mask_id = self.token2id[self.mask_token]

        self.do_lower_case = do_lower_case

    def _load_bert_vocab(self, vocab_file):
        vocab = {}
        idx = 0
        with open(vocab_file, mode='rt', encoding='utf-8') as fin:
            for line in fin:
                word = line.rstrip('\n')
                vocab[word] = idx
                idx += 1
        return vocab

    def encode(self, text, add_cls=True, add_sep=True, **kwargs):
        tokens, ids, type_ids, attention_mask, offsets = [], [], [], [], []
        if self.do_lower_case:
            text = str(text).lower()
        for idx, char in enumerate(text):
            tokens.append(char)
            ids.append(self.token2id.get(char, self.unk_id))
            type_ids.append(0)
            attention_mask.append(1)
            offsets.append((idx, idx + 1))

        if add_cls:
            tokens.insert(0, self.cls_token)
            ids.insert(0, self.cls_id)
            type_ids.insert(0, 0)
            attention_mask.insert(0, 1)
            offsets.insert(0, (0, 0))

        if add_sep:
            tokens.append(self.sep_token)
            ids.append(self.sep_id)
            type_ids.append(0)
            attention_mask.append(1)
            offsets.append((0, 0))

        encoding = TokenizerEncoding(
            text=text,
            tokens=tokens,
            ids=ids,
            type_ids=type_ids,
            attention_mask=attention_mask,
            offsets=offsets)
        return encoding

    def decode(self, ids, **kwargs):
        return [self.id2token.get(_id, self.unk_token) for _id in ids]
