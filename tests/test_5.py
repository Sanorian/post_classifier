import pytest
import requests

def check_space():
    request = requests.post("http://localhost:8080/classify", json={"text": "Space exploration is a fascinating field."})
    return request.json()

def test_space_classification():
    result = check_space()['category']
    assert result == "sci.space"
