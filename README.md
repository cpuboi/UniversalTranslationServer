# Translation Server #

This is a FastAPI based REST server that translates text offline.
As of now m2m100 is supported.
https://huggingface.co/docs/transformers/model_doc/m2m_100

## Settings ##
./translation_server/core/config.py contains all model file paths



### Usage ###
```
curl -X 'POST' \
  'http://localhost:7890/translate/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input_language": "ru",
  "output_language": "en",
  "input_text": "ВГР — это тип высокотемпературного реактора (ВТР), который теоретически может иметь температуру на выходе 1000 °C",
  "translation_model": "opus-mt"
}'                   
```


