FROM python:3.11.7-bookworm

WORKDIR /research-index

ADD requirements.txt /research-index/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ADD . /research-index

EXPOSE 8000

CMD ["fastapi", "run", "main.py", \
     "--port", "8000", \
     "--workers", "4", \
     "--proxy-headers"]