FROM python:3.11-slim
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user
ENV PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY --chown=user . $HOME/app
VOLUME /data
EXPOSE 22222
CMD ["python", "-m", "apis.chat_api"]