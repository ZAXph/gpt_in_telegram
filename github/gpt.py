import requests
from config import *


def gpt_processing(user_content):
    resp = requests.post(
        'http://localhost:1234/v1/chat/completions',
        headers={"Content-Type": "application/json"},

        json={
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            "temperature": 1,
            "max_tokens": MAX_TOKEN,
        }
    )
    return resp


def gpt_processing_next(user_content, text):
    resp = requests.post(
        'http://localhost:1234/v1/chat/completions',
        headers={"Content-Type": "application/json"},

        json={
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content + text}
            ],
            "temperature": 1,
            "max_tokens": MAX_TOKEN,
        }
    )
    return resp
