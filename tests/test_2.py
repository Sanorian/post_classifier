import pytest
import requests

def check_baseball():
    request = requests.post("http://localhost:8080/classify", json={"text": "Baseball is a popular sport in the United States."})
    return request.json()

def test_baseball_classification():
    result = check_baseball()['category']
    assert result == "rec.sport.baseball"
