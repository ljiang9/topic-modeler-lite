# topic-modeler-lite

简易**主题模型**，纯 Python 实现、无需 LLM。基于词共现关系聚类得到若干主题及 top 词。

## 方法

1. 分词并统计词频；
2. 构建词-词共现矩阵（同一文档中共现）；
3. k-means++ 式分散选择主题种子词；
4. 把其余词分配给共现最强的种子，形成主题；
5. 输出每个主题的 top 关键词。

## 快速开始

```bash
python3 cli.py "足球 比赛 进球 球迷" "算法 芯片 数据 模型"
# 主题 1（种子词「比赛」）：比赛、球迷、足球、进球
# 主题 2（种子词「芯片」）：芯片、模型、数据、算法
```

## 使用示例

```bash
# 指定主题数与每主题词数
python3 cli.py -t 3 -w 6 doc1.txt...
```

## 无 API Key 如何运行

本工具**完全不需要 API Key**，主题抽取为本地共现统计。

## 目录结构

```
topic-modeler-lite/
├── modeler.py    # 共现矩阵、分散选种、主题分配、报告
├── cli.py        # 命令行入口
├── tests/
│   └── test_modeler.py
├── README.md
├── LICENSE
└── .gitignore
```

## 测试

```bash
python3 -m unittest discover -s tests
```

## 许可证

[MIT](./LICENSE)
