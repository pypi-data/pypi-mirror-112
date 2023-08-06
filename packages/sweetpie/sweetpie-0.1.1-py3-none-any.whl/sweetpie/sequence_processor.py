import abc
import logging
import os

from .tokenizers import AbstractTokenizer, ChineseBertCharTokenizer

SEP_CHARACTERS = set(['，', '。', '：', '？', '！', '；', '’', ',', ':', '?', '!', ';'])


class ChineseCharSequenceProcessor:

    def __init__(self, sep_chars=None, **kwargs):
        super().__init__()
        self.sep_chars = sep_chars or SEP_CHARACTERS

    def process(self, sequence, max_sequence_length=512, sliding_window_size=256, soft_sliding=True, **kwargs):
        if not soft_sliding:
            hard_examples = self._hard_process(
                sequence,
                max_sequence_length=max_sequence_length,
                sliding_window_size=sliding_window_size,
                **kwargs)
            return hard_examples
        soft_examples = self._soft_process(
            sequence,
            max_sequence_length=max_sequence_length,
            sliding_window_size=sliding_window_size,
            **kwargs)
        return soft_examples

    def _hard_process(self, sequence, max_sequence_length=512, sliding_window_size=256, **kwargs):
        examples = []
        for idx in range(0, len(sequence), sliding_window_size):
            start, end = idx, idx + max_sequence_length
            examples.append({
                'offset': idx,
                'text': sequence[start: end]
            })
            if end > len(sequence):
                break
        return examples

    def _soft_process(self, sequence, max_sequence_length=512, sliding_window_size=256, **kwargs):
        examples = []

        prev_start, prev_end = 0, 0
        while prev_end < len(sequence):
            cur_start = prev_end
            # cur_end未必是位于句子结尾，需要往前移动
            cur_end = cur_start + max_sequence_length
            pos = self._find_left_seperator(cur_end, sequence)
            cur_end = pos + 1 if pos is not None and pos > cur_start else cur_end
            examples.append({
                'offset': cur_start,
                'text': sequence[cur_start: cur_end]
            })
            prev_start = cur_start
            prev_end = cur_end
            if cur_end > len(sequence):
                break

        return examples

    def _find_left_seperator(self, idx, sequence):
        if idx >= len(sequence):
            idx = len(sequence)
        left = idx - 1
        while left > 0:
            if sequence[left] in self.sep_chars:
                return left
            left -= 1
        return None


class ChineseCharSequencePairProcessor(ChineseCharSequenceProcessor):

    def __init__(self, sep_chars=None, **kwargs):
        super().__init__(sep_chars=sep_chars, **kwargs)

    def process(self,
                seqa,
                seqb,
                max_seqa_length=256,
                max_sequence_length=512,
                sliding_window_size=256,
                soft_sliding=True,
                **kwargs):
        if len(seqa) > max_seqa_length:
            raise ValueError('seqa is too long!')
        max_seqb_length = max_sequence_length - max_seqa_length
        seqb_examples = super().process(
            sequence=seqb,
            max_sequence_length=max_seqb_length,
            sliding_window_size=sliding_window_size,
            soft_sliding=soft_sliding,
            **kwargs)

        examples = []
        for e in seqb_examples:
            examples.append({
                'seqa': seqa,
                'seqb_offset': e['offset'],
                'seqb_text': e['text']
            })
        return examples
