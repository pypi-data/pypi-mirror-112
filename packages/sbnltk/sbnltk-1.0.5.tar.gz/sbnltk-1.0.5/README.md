# SBNLTK
Bangla NLP toolkit. Different types of NLP models were implemented here.\
Last version : **1.0.0**

## INSTALLATION
### PYPI INSTALLATION
```commandline
pip3 install sbnltk
```
### MANUAL INSTALLATION FROM GITHUB

```commandline

```

## TASKS AND MODELS
|            TASK           |                               MODEL                               |    ACCURACY    |         DATASET         | About | Code DOCS |
|:-------------------------:|:-----------------------------------------------------------------:|:--------------:|:-----------------------:|:-----:|:---------:|
|        Preprocessor       | Punctuation, Stop Word, DUST removal Word normalization, others.. |     ------     |          -----          |       |           |
|      Word tokenizers      |               basic tokenizers Customized tokenizers              |      ----      |           ----          |       |           |
|    Sentence tokenizers    |      Basic tokenizers Customized tokenizers Sentence Cluster      |      -----     |          -----          |       |           |
|          Stemmer          |                             StemmerOP                             |      85.5%     |           ----          |       |           |
|     Sentiment Analysis    |                         logisticRegression                        |      88.5%     |         20,000+         |       |           |
|                           |                             LinearSVC                             |      82.3%     |         20,000+         |       |           |
|                           |                      Multilnomial_naive_bayes                     |      84.1%     |         20,000+         |       |           |
|                           |                           Random Forest                           |      86.9%     |         20,000+         |       |           |
|                           |                                BERT                               |      93.2%     |         20,000+         |       |           |
|         POS tagger        |                           Static method                           |      55.5%     |     1,40,973  words     |       |           |
|                           |                      SK-LEARN classification                      |      81.2%     |     6,000+ sentences    |       |           |
|                           |                        BERT-Multilingual-Cased                    |      69.2%     |          6,000+         |       |           |
|                           |                     BERT-Multilingual-Uncased                     |      76.7%     |          6,000+         |       |           |
|         NER tagger        |                           Static method                           |      65.3%     |     4,08,837 Entity     |       |           |
|                           |                      SK-LEARN classification                      |      81.2%     |         65,000+         |       |           |
|                           |                             BERT-Cased                            |      79.2%     |         65,000+         |       |           |
|                           |                       BERT-Mutilingual-Cased                      |      75.5%     |         65,000+         |       |           |
|                           |                     BERT-Multilingual-Uncased                     |      87.5%     |         65,000+         |       |           |
|       Word Embedding      |             Gensim-word2vec-100D- 1,00,00,000+ tokens             |        -       | 2,00,00,000+  sentences |       |           |
|                           |               Glove-word2vec-100D- 2,30,000+ tokens               |        -       |    5,00,000 sentences   |       |           |
|                           |                  fastext-word2vec-200D 3,00,000+                  |        -       |    5,00,000 sentences   |       |           |
|     Sentence Embedding    |                   Contextual sentence embedding                   |        -       |          -----          |       |           |
|                           |                      Transformer embedding_hd                     |        -       |   3,00,000+ human data  |       |           |
|                           |                      Transformer embedding_gd                     |        -       |  3,00,000+ google data  |       |           |
| Extractive  Summarization |                        Feature-based based                        | 70.0% f1 score |          ------         |       |           |
|                           |                Transformer sentence sentiment Based               |      67.0%     |          ------         |       |           |
|                           |                Word2vec--sentences contextual Based               |      60.0%     |          -----          |       |           |
|    Bi-lingual projects    |             google translator with large data detector            |      ----      |           ----          |       |           |
|   Information Extraction  |                        Static word features                       |        -       |                         |       |           |
|                           |                      Semantic and contextual                      |        -       |                         |       |           |




|              Task              |    Version   |
|:------------------------------:|:------------:|
|     Coreference Resolution     |    v1.1.0    |
|      Language translation      |    V1.1.0    |
|      Masked Language model     |    V1.1.0    |
| Information retrieval Projects |    V1.1.0    |
|       Entity Segmentation      |    v1.3.0    |
|   Factoid Question Answering   |    v1.2.0    |
|     Question Classification    |    v1.2.0    |
|    sentiment Word embedding    |    v1.3.0    |
|     So many others features    | coming soon  |
