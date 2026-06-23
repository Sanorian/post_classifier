import pytest
import requests

def check_medicine():
    request = requests.post("http://localhost:8080/classify", json={"text": "He had an award for his research in medicine."})
    return request.json()

def test_medicine_classification():
    result = check_medicine()['category']
    assert result == "sci.med"
