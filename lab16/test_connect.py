# test_connection.py
from gigachat import GigaChat
from token_dla_gigachat import token

with GigaChat(credentials=token, verify_ssl_certs=False) as giga:
    response = giga.chat("Привет! Ты работаешь?")
    print(response.choices[0].message.content)