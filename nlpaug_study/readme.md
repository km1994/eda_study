# 【关于 nlpaug 数据增强】 那些你不知道的事

- nlpaug 项目：https://github.com/makcedward/nlpaug

## 一、nlpaug 介绍

一、nlpaug 库可以帮助你为你的 nlp 项目 做数据增强 。访问此 [简介](https://zhuanlan.zhihu.com/p/150600950)以了解 NLP 中的数据增强。 Augmenter 是增强的基本元素，而 Flow 是将多个增强器编排在一起的管道。

## 二、nlpaug 安装

- requirement
  - python >= 3.5

- 简单安装

```s
    pip install numpy requests nlpaug
```

- 直接从 github 安装最新版本（包括 BETA 功能）

```s
    pip install numpy git+https://github.com/makcedward/nlpaug.git
```

- conda 安装

```s
    conda install -c makcedward nlpaug
```

- 如果您使用 BackTranslationAug、ContextualWordEmbsAug、ContextualWordEmbsForSentenceAug 和 AbstSummAug，则还要安装以下依赖项

```s
    pip install torch>=1.6.0 transformers>=4.0.0 sentencepiece
```

- 如果您使用 LambadaAug，还要安装以下依赖项

```s
    pip install simpletransformers>=0.61.10
```

- 如果使用 AntonymAug、SynonymAug，还要安装以下依赖

```s
    pip install nltk>=3.4.5
```

- 如果您使用 WordEmbsAug（word2vec、glove 或 fasttext），请先下载预训练模型

```s
    from nlpaug.util.file.download import DownloadUtil
    DownloadUtil.download_word2vec(dest_dir='.') # Download word2vec model
    DownloadUtil.download_glove(model_name='glove.6B', dest_dir='.') # Download GloVe model
    DownloadUtil.download_fasttext(model_name='wiki-news-300d-1M', dest_dir='.') # Download fasttext model
```

- 如果您使用 WordEmbsAug（word2vec、glove 或 fasttext），请先下载预训练模型

```s
    from nlpaug.util.file.download import DownloadUtil
    DownloadUtil.download_word2vec(dest_dir='.') # Download word2vec model
    DownloadUtil.download_glove(model_name='glove.6B', dest_dir='.') # Download GloVe model
    DownloadUtil.download_fasttext(model_name='wiki-news-300d-1M', dest_dir='.') # Download fasttext model
```

- 如果您使用 SynonymAug (PPDB)，请从以下 URI 下载文件。如果您从其他网站获取 PPDB 文件，您可能无法运行增强器

```s
    http://paraphrase.org/#/download
```

- 如果您使用 PitchAug、SpeedAug 和 VtlpAug，则还要安装以下依赖项

```s
    pip install librosa>=0.7.1 matplotlib
```

## 三、nlpaug 快速入门




## 参考

1. [nlpaug](https://github.com/makcedward/nlpaug)
