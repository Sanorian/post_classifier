import pytest
import requests

def check_guns():
    request = requests.post("http://localhost:8080/classify", json={"text": "Guns are a controversial topic."})
    return request.json()

def test_guns_classification():
    result = check_guns()['category']
    assert result == "talk.politics.guns"
