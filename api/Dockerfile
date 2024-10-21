# author: alvertogit
# copyright: 2024

FROM python:3.12-slim-bookworm
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN python3 -m venv .
RUN python3 -m pip install --no-cache-dir -r requirements.txt
EXPOSE 8888
CMD uvicorn main:app --host 0.0.0.0 --port 8888
