import json
import unittest

from sweetpie.sequence_processor import (ChineseCharSequencePairProcessor,
                                         ChineseCharSequenceProcessor)

sequences = [
    '静脉,动脉的血压太大,一旦破裂就无法及时止住,会死人的,而毛细血管的直径还不到0.1毫米,无法下针。人体内的血管总长是多少?是九万六千公里,比尼罗河长五倍多。...',
    '经审理查明:原告曹0与被告张x1原5夫妻关系2001年5月27日,原、被告生育一女张x62011年7月21日,原、被告因夫妻感情破裂,在重庆市荣昌县人民法院调解离婚,调解书载明:“原、被告之女张x6随被告张x1生活”原、被告离婚后又自行协商,约定小孩张x6暂由原告代管,被告每月向原告支付张x6的生活费800元因此,张x6一直随原告生活至今,期间被告未依照约定按时向原告支付张x6的生活费另查明:张x6现在荣昌县城西小学上学,为城镇居民户口原告曹0系重庆博耐特压铸有限公司职工,收入比较稳定,现已再婚,其与丈夫何祖君共同购买了位于荣昌县昌元街道昌州大道西段的房屋一套本案在审理过程中,本院依法对张x6作了询问笔录,张x6称从父母离婚后其一直随母亲生活,只在每年暑假到父亲家里玩耍一段时间,现在自己愿意随母亲曹0生活上述事实,有原告陈述,被告答辩状,常住人口登记卡,重庆市荣昌县人民法院作出的(2011)荣4民初字第1929号民事调解书,原、被告签订的协议,结婚证,房产证,劳动合同,重庆市基本养老保险个人账户信息表,对张x6的询问笔录等证据予以证实'
]


class SequenceProcessorTest(unittest.TestCase):

    def test_chinese_char_sequence_processor(self):
        p = ChineseCharSequenceProcessor()

        print()
        for seq in sequences:
            hard_examples = p.process(seq, max_sequence_length=256, sliding_window_size=128, soft_sliding=False)
            soft_examples = p.process(seq, max_sequence_length=256, sliding_window_size=128, soft_sliding=True)
            print('hard examples: ')
            for e in hard_examples:
                print(json.dumps(e, ensure_ascii=False))
            print('soft examples; ')
            for e in soft_examples:
                print(json.dumps(e, ensure_ascii=False))
            print()

    def test_chinese_char_sequence_pair_processor(self):
        p = ChineseCharSequencePairProcessor()
        print()

        seqa = sequences[0]
        seqb = sequences[1]
        hard_examples = p.process(
            seqa,
            seqb,
            max_seqa_length=128,
            max_sequence_length=256,
            sliding_window_size=128,
            soft_sliding=False)
        soft_examples = p.process(
            seqa,
            seqb,
            max_seqa_length=128,
            max_sequence_length=256,
            sliding_window_size=128,
            soft_sliding=True)
        print('hard examples: ')
        for e in hard_examples:
            print(json.dumps(e, ensure_ascii=False))
        print('soft examples; ')
        for e in soft_examples:
            print(json.dumps(e, ensure_ascii=False))
        print()


if __name__ == "__main__":
    unittest.main()
