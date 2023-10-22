set -eu

#uvicorn main:app --reload --host 0.0.0.0 --port 7890
uvicorn main:app  --host 0.0.0.0 --port 7890

