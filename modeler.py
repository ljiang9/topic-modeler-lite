"""topic-modeler-lite — 简易主题模型（纯 Python，无 LLM）。

基于词共现：统计词与词在同一文档中共现的强度，选取高频词作主题种子，
把其余词分配给共现最强的种子，得到若干主题及其 top 词。
零第三方依赖。
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict

_EN_RE = re.compile(r"[a-zA-Z]+")
STOPWORDS = {"the", "a", "an", "is", "are", "of", "and", "to", "in", "on",
             "的", "了", "和", "是", "在", "与", "及", "或"}


def tokenize(text: str) -> list[str]:
    # 英文整词；中文按「连续汉字段」切分（空格分隔即为词组）
    toks = _EN_RE.findall(text.lower())
    toks += re.findall(r"[\u4e00-\u9fff]+", text)
    return [t for t in toks if t not in STOPWORDS and len(t) > 1]


def extract_topics(docs: list[str], n_topics: int = 2,
                   top_words: int = 5) -> list[dict]:
    """从文档集合抽取主题。

    返回 [{"seed": 种子词, "top_words": [(词, 强度), ...]}, ...]
    """
    doc_tokens = [tokenize(d) for d in docs]
    freq: Counter = Counter()
    for toks in doc_tokens:
        freq.update(sorted(set(toks)))
    if not freq:
        return []

    co: dict[str, Counter] = defaultdict(Counter)
    for toks in doc_tokens:
        uniq = sorted(set(toks))
        for i in range(len(uniq)):
            for j in range(i + 1, len(uniq)):
                a, b = uniq[i], uniq[j]
                co[a][b] += 1
                co[b][a] += 1

    vocab = freq.most_common()
    seeds: list[str] = [vocab[0][0]]
    while len(seeds) < min(n_topics, len(vocab)):
        best_w, best_dist = None, -1.0
        for w, _ in vocab:
            if w in seeds:
                continue
            dist = sum(co[w].get(s, 0) for s in seeds)
            if dist < best_dist or best_w is None:
                best_w, best_dist = w, dist
        seeds.append(best_w)

    assign: dict[str, list[str]] = {s: [s] for s in seeds}
    for w, _ in vocab:
        if w in seeds:
            continue
        best_seed = seeds[0]
        best_score = -1.0
        for s in seeds:
            score = co[w].get(s, 0)
            if score > best_score:
                best_score = score
                best_seed = s
        assign[best_seed].append(w)

    topics = []
    for s in seeds:
        members = assign[s]
        scored = sorted(
            ((w, freq[w] + sum(co[w].get(m, 0) for m in members)) for w in members),
            key=lambda x: x[1], reverse=True,
        )
        topics.append({"seed": s, "top_words": scored[:top_words]})
    return topics


def topics_report(docs: list[str], n_topics: int = 2,
                  top_words: int = 5) -> str:
    topics = extract_topics(docs, n_topics=n_topics, top_words=top_words)
    if not topics:
        return "（无有效主题）"
    lines = [f"=== 简易主题模型报告（{len(topics)} 个主题）==="]
    for i, t in enumerate(topics, 1):
        words = "、".join(w for w, _ in t["top_words"])
        lines.append(f"主题 {i}（种子词「{t['seed']}」）：{words}")
    return "\n".join(lines)
