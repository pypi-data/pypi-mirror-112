## Sani NLU
This is a module that implements the NLU component for the Sani Chatbot

## How to integrate with Sani

1. Install dependencies:

```bash
pip install sani_nlu
```

2. Configuration

- Flair Extractor
```yml

pipeline:
  - name: sani_nlu.VietnameseTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: CountVectorsFeaturizer
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4
  - name: DIETClassifier
    epochs: 50
    constrain_similarities: true
  - name: sani_nlu.FlairExtractor
  - name: EntitySynonymMapper
  - name: FallbackClassifier
    threshold: 0.8
    ambiguity_threshold: 0.1
```