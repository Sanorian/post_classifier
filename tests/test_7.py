import pytest
import requests

def check_graphics():
    request = requests.post("http://localhost:8080/classify", json={"text": "Graphics design is a creative field."})
    return request.json()

def test_graphics_classification():
    result = check_graphics()['category']
    assert result == "comp.graphics"
