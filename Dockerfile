FROM python:3.12-slim

WORKDIR /app

COPY ./app/* .
COPY ./tools/* ./tools/
COPY ./graph/* ./graph/
COPY ./vector_db/* ./vector_db/
COPY ./ui/* .

COPY requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

COPY run.sh .
ENTRYPOINT ["bash", "run.sh"]