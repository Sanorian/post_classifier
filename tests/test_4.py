import pytest
import requests

def check_hockey():
    request = requests.post("http://localhost:8080/classify", json={"text": "Hockey is a popular sport in Canada."})
    return request.json()

def test_hockey_classification():
    result = check_hockey()['category']
    assert result == "rec.sport.hockey"
