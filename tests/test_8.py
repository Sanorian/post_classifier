import pytest
import requests

def check_guns():
    request = requests.post("http://localhost:8080/classify", json={"text": ""})
    return request.json()

def test_guns_classification():
    result = check_guns()['detail']
    assert result == "Пустой текст не может быть классифицирован"
