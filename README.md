## Bing-Chat-API

A successor to [EdgeGPT](https://github.com/acheong08/EdgeGPT) by [acheong08](https://github.com/acheong08).

**Note: This project is in rapid progress, and currently is not ready to be used in production.**

After completing some key features, I would focus on the quick deployment of this project.

## Install dependencies

```bash
# pipreqs . --force --mode no-pin
pip install -r requirements.txt
```

## Run

```bash
python -m apis.chat_api
```

## Docker Build

```bash
sudo docker build -t bing-chat-api:1.0 . --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy
```

## Example

Command Line:

![Bing-Chat-API-CLI](./docs/bing-chat-api-cli.png)