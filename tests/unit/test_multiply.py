from fastapi.testclient import TestClient
from src.multiply_service.multiply import app
import math

client = TestClient(app)

def test_multiply_normal_cases():
    assert client.post("/multiply", json={"a": 2, "b": 3}).json() == {"result": 6}
    assert client.post("/multiply", json={"a": -4, "b": 5}).json() == {"result": -20}
    assert client.post("/multiply", json={"a": 0, "b": 100}).json() == {"result": 0}

def test_multiply_extreme_cases():
    assert client.post("/multiply", json={"a": int(1e5), "b": int(1e5)}).json() == {"result": int(1e10)}
    assert client.post("/multiply", json={"a": int(1e10), "b": 0}).json() == {"result": 0}

def test_multiply_commutativity():
    a, b = 7, 3
    r1 = client.post("/multiply", json={"a": a, "b": b}).json()
    r2 = client.post("/multiply", json={"a": b, "b": a}).json()
    assert r1 == r2

def test_multiply_boolean_input():
    assert client.post("/multiply", json={"a": True, "b": 5}).json() == {"result": 5}
    assert client.post("/multiply", json={"a": False, "b": 10}).json() == {"result": 0}

def test_multiply_invalid_input():
    res = client.post("/multiply", json={"a": "x", "b": 3})
    assert res.status_code == 422
    res = client.post("/multiply", json={"a": {}, "b": 3})
    assert res.status_code == 422
    res = client.post("/multiply", json={"a": None, "b": 3})
    assert res.status_code == 422
