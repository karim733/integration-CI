from fastapi.testclient import TestClient
from src.add_service.app import app
import math

client = TestClient(app)

def test_add_normal_cases():
    assert client.post("/add", json={"a": 2, "b": 3}).json() == {"result": 5}
    assert client.post("/add", json={"a": -4, "b": 5}).json() == {"result": 1}
    assert client.post("/add", json={"a": 0, "b": 100}).json() == {"result": 100}

def test_add_extreme_cases():
    assert client.post("/add", json={"a": int(1e10), "b": int(1e10)}).json() == {"result": int(2e10)}
    assert client.post("/add", json={"a": -int(1e10), "b": 1}).json() == {"result": -int(1e10)+1}

def test_add_commutativity():
    a, b = 7, 3
    r1 = client.post("/add", json={"a": a, "b": b}).json()
    r2 = client.post("/add", json={"a": b, "b": a}).json()
    assert r1 == r2

def test_add_boolean_input():
    assert client.post("/add", json={"a": True, "b": 2}).json() == {"result": 3}
    assert client.post("/add", json={"a": False, "b": 10}).json() == {"result": 10}

def test_add_invalid_input():
    res = client.post("/add", json={"a": "x", "b": 3})
    assert res.status_code == 422
    res = client.post("/add", json={"a": [1,2], "b": 3})
    assert res.status_code == 422
    res = client.post("/add", json={"a": None, "b": 3})
    assert res.status_code == 422
