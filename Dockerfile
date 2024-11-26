FROM python:3.11.7-bookworm

WORKDIR /research-index

ADD requirements.txt /research-index/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ADD . /research-index

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]