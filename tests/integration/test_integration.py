import requests
import pytest

ADD_URL = "http://localhost:5000/add"
MULTIPLY_URL = "http://localhost:5001/multiply"

def test_add_then_multiply():
    r1 = requests.post(ADD_URL, json={"a": 2, "b": 3})
    assert r1.status_code == 200
    total = r1.json()["result"]

    r2 = requests.post(MULTIPLY_URL, json={"a": total, "b": 4})
    assert r2.status_code == 200
    assert r2.json()["result"] == 20

def test_multiply_then_add():
    r1 = requests.post(MULTIPLY_URL, json={"a": 3, "b": 4})
    product = r1.json()["result"]

    r2 = requests.post(ADD_URL, json={"a": product, "b": 2})
    assert r2.json()["result"] == 14

def test_nested_chaining():
    r1 = requests.post(ADD_URL, json={"a": 1, "b": 2}).json()["result"]
    r2 = requests.post(ADD_URL, json={"a": 3, "b": 4}).json()["result"]
    r3 = requests.post(MULTIPLY_URL, json={"a": r1, "b": r2})
    assert r3.json()["result"] == 21

def test_distributive_property():
    a, b, c = 2, 3, 4
    r1 = requests.post(ADD_URL, json={"a": b, "b": c}).json()["result"]
    left = requests.post(MULTIPLY_URL, json={"a": a, "b": r1}).json()["result"]

    ab = requests.post(MULTIPLY_URL, json={"a": a, "b": b}).json()["result"]
    ac = requests.post(MULTIPLY_URL, json={"a": a, "b": c}).json()["result"]
    right = requests.post(ADD_URL, json={"a": ab, "b": ac}).json()["result"]

    assert left == right

def test_invalid_chained_inputs():
    r = requests.post(ADD_URL, json={"a": "x", "b": 2})
    assert r.status_code == 422

    r = requests.post(MULTIPLY_URL, json={"a": None, "b": 3})
    assert r.status_code == 422
