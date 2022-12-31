import json
import requests
import logging



template_api_url = "https://web.audioteka.com/pl/do-uslyszenia-w-klubie.html?v=13&id=%s"
logging.basicConfig(level=logging.INFO)
logging.addLevelName(logging.INFO, "\x1b[32m%s\x1b[32m" % logging.getLevelName(logging.INFO))
def get_json(api_url: str) -> dict:
    r = requests.get(api_url)
    return json.loads(r.text)

def get_all_titles() -> list[str]:
    total_titles = []
    offset = 30
    max_title = 1000
    temp_last_id_from = ''
    for i in range(max_title):
        url = template_api_url % temp_last_id_from
        logging.info(f"process: {url}")
        items_list = get_json(url)
        for i, item_json in enumerate(items_list):
            if i == offset - 1:
                temp_last_id_from = item_json.get("id")
            total_titles.append(item_json.get("name"))
        # fuse: for end forloop when we don't have no more items
        if len(items_list) < offset - 2:
            break
    return total_titles

def show_all_title(titles: list[str]):
    for title in titles:
        print(title)
    print("*"*10)
    print(len(titles))
titles = get_all_titles()
show_all_title(titles)
