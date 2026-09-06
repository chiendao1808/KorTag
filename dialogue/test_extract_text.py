import sys
import types
import unittest


class _Komoran:
    def __init__(self, **_kwargs):
        pass

    def pos(self, text):
        return [(text, "NNG")]


fake_konlpy = types.ModuleType("konlpy")
fake_tag = types.ModuleType("konlpy.tag")
fake_tag.Komoran = _Komoran
fake_konlpy.tag = fake_tag
sys.modules.setdefault("konlpy", fake_konlpy)
sys.modules.setdefault("konlpy.tag", fake_tag)

from dialogue.extract_text import merge_incomplete_utterances


class MergeIncompleteUtterancesTest(unittest.TestCase):
    def test_preserves_ordered_speakers_and_trailing_fragment(self):
        utterances = [
            {"speaker_id": "A", "form": "Hôm nay trời"},
            {"speaker_id": "B", "form": "rất đẹp."},
            {"speaker_id": "A", "form": "Tôi nghĩ"},
            {"speaker_id": "A", "form": "chúng ta nên đi"},
            {"speaker_id": "B", "form": "ngay!"},
            {"speaker_id": "C", "form": "Câu cuối chưa hoàn chỉnh"},
        ]

        self.assertEqual(
            merge_incomplete_utterances(utterances),
            [
                {"speaker_id": "A,B", "form": "Hôm nay trời rất đẹp."},
                {"speaker_id": "A,A,B", "form": "Tôi nghĩ chúng ta nên đi ngay!"},
                {"speaker_id": "C", "form": "Câu cuối chưa hoàn chỉnh"},
            ],
        )

    def test_detects_terminal_punctuation_before_trailing_tags(self):
        utterances = [
            {"speaker_id": "A", "form": "Câu đầu.<br>"},
            {"speaker_id": "B", "form": "Câu thứ hai?"},
        ]

        self.assertEqual(
            merge_incomplete_utterances(utterances),
            [
                {"speaker_id": "A", "form": "Câu đầu.<br>"},
                {"speaker_id": "B", "form": "Câu thứ hai?"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
