import pytest
import requests

def check_health():
    request = requests.get("http://localhost:8080/health")
    return request.json()

def test_health_endpoint():
    health_status = check_health()
    assert health_status["status"] == "ok", "Health check failed. Model or vectorizer may not be loaded."