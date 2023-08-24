# Translation Server #

This is a FastAPI based REST server that translates text offline.  
Supported models:
* m2m100
* nllb
* opus-mt



### Settings without docker ###
./translation_server/core/config.py contains all model file paths


### Docker settings ###
Edit docker-compose.yml to change volume directory to the one where models exist on the harddrive.
Point out this directory in the /app volume if you want to be able to edit code on the fly.

If you want to build the docker container with the python code embedded, uncomment these lines in Dockerfile:
``` 
#copy translation_server translation_server
#copy main.py main.py
```

### Download Models ###
* Install git-lfs support
* Opus-mt
  info: https://github.com/Helsinki-NLP/Tatoeba-Challenge/tree/master/models/dan-eng  
  `git clone https://huggingface.co/Helsinki-NLP/opus-mt-da-en/`
* Edit the translation_server/api/core/config.py file depending on Opus-mt file or specific model file 

### Usage ###
```
curl -X 'POST' \
  'http://localhost:7890/translate/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input_language": "da",
  "output_language": "en",
  "input_text": "Vanløse IF er en klub for begge køn og har i 2013 godt 1.000 medlemmer",
  "translation_model": "opus-mt"
}'                   
```
It is possible to select model, if you choose "default" TranslationServer will pick opus-mt, nllb or m2m100 in that order.  
#### Interactive client ####
`./client.py` makes it possible to query the webserver from the terminal. 

