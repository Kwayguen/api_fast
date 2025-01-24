
FROM continuumio/miniconda3

WORKDIR /home/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY api.py .
COPY model.pkl .

RUN pip install -r requirements.txt

CMD uvicorn api:app --port $PORT --host 127.0.0.1



