"""命令行：python3 cli.py doc1 doc2 ..."""
import argparse
import json

from modeler import extract_topics, topics_report


def main(argv=None):
    p = argparse.ArgumentParser(description="topic-modeler-lite 简易主题模型")
    p.add_argument("-t", "--topics", type=int, default=2, help="主题个数")
    p.add_argument("-w", "--top-words", type=int, default=5, help="每主题 top 词数")
    p.add_argument("--json", action="store_true")
    p.add_argument("docs", nargs="+", help="文档集合")
    args = p.parse_args(argv)

    if args.json:
        print(json.dumps(extract_topics(args.docs, args.topics, args.top_words),
                         ensure_ascii=False, indent=2))
    else:
        print(topics_report(args.docs, args.topics, args.top_words))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
