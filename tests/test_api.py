import requests

from src import config
from src.domain import schemas, model 

def test_happy_path_ping():
    url = f"{config.get_api_url()}/ping"
    r = requests.get(url)
    assert r.status_code==200
    assert r.json()["title"] == "pong"


# def test_add_title_to_source():
    # data = {"title":"Marian"}
    # url = f"{config.get_api_url()}/send_title"
    # r = requests.post(url, json=data)
    # assert r.status_code == 201
    # assert r.json()["title"] == "Marian"

def test_unhappy_path_trying_add_same_title_twice():
    data = {"title":"Marian"}
    url = f"{config.get_api_url()}/send_title"
    r = requests.post(url, json=data)
    assert r.status_code == 400
    assert r.json()["detail"] == f"title: Marian is in db!!"



