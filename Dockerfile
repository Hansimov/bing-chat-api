FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
VOLUME /data
EXPOSE 22222
CMD ["python", "-m", "apis.chat_api"]