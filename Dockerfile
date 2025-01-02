FROM python:3.11.7-bookworm

WORKDIR /research-index

ADD requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ADD . .

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", \
     "--port", "8000", \
     "--workers", "4", \
     "--proxy-headers"]