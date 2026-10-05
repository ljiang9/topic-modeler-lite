"""topic-modeler-lite 单元测试。运行：python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modeler import extract_topics, topics_report, tokenize  # noqa: E402


class TestTokenize(unittest.TestCase):
    def test_stopwords(self):
        toks = tokenize("the football and basketball of players")
        self.assertIn("football", toks)
        self.assertNotIn("the", toks)


class TestTopics(unittest.TestCase):
    def test_two_distinct_topics(self):
        docs = [
            "football basketball match player champion league goal fan",
            "football team score win stadium coach",
            "algorithm machinelearning chip software data computer model",
            "neural network training dataset code programmer",
        ]
        topics = extract_topics(docs, n_topics=2, top_words=4)
        self.assertEqual(len(topics), 2)
        seeds = {t["seed"] for t in topics}
        self.assertEqual(len(seeds), 2)
        allwords = [w for t in topics for w, _ in t["top_words"]]
        self.assertTrue(any("football" in w or "match" in w for w in allwords))
        self.assertTrue(any("algorithm" in w or "chip" in w for w in allwords))

    def test_empty(self):
        self.assertEqual(extract_topics([], n_topics=2), [])

    def test_report(self):
        rpt = topics_report(["football match", "algorithm chip"], n_topics=2)
        self.assertIn("主题", rpt)


if __name__ == "__main__":
    unittest.main()
