## Audio_teka scrap
### Discription
####Problem:
In a certain streaming portal wanting to get information about what  audiobooks titles are in the subscription, the owner of the portal refers us to the url. The page shows the titles that are in the subscription. But in order to see all the content, you have to scroll through it, as the content recharges. We are unable to determine how long it will take. Which is frustrating.
#### Solution:
Create a scrape that is able to retrieve audiobook titles from the given url.
Then load the acquired titles into the database connect to the API, create an endpoint in the API which is able to query the DB and acquire the title of the searched book which is in the subscription
#### Technology stack:
#### Back-end:
- python
- fastapi API
- postgres DB
- pytes (for tests)
#####python library:
```
Package             Version
------------------- ---------------
anyio               3.6.2
async-generator     1.10
attrs               22.2.0
beautifulsoup4      4.11.1
black               22.12.0
certifi             2022.12.7
charset-normalizer  2.1.1
chromedriver-binary 106.0.5249.61.0
click               8.1.3
exceptiongroup      1.1.0
fastapi             0.85.2
greenlet            2.0.1
h11                 0.14.0
idna                3.4
iniconfig           1.1.1
Jinja2              3.1.2
MarkupSafe          2.1.1
mypy-extensions     0.4.3
numpy               1.24.1
outcome             1.2.0
packaging           22.0
pandas              1.5.2
pathspec            0.10.3
pip                 22.2.2
platformdirs        2.6.2
pluggy              1.0.0
psycopg2-binary     2.9.5
pydantic            1.10.4
PySocks             1.7.1
pytest              7.2.0
python-dateutil     2.8.2
pytz                2022.7
requests            2.28.1
selenium            4.7.2
setuptools          65.3.0
six                 1.16.0
sniffio             1.3.0
sortedcontainers    2.4.0
soupsieve           2.3.2.post1
SQLAlchemy          1.4.45
starlette           0.20.4
tomli               2.0.1
trio                0.22.0
trio-websocket      0.9.2
typing_extensions   4.4.0
urllib3             1.26.13
uvicorn             0.18.3
wheel               0.37.1
wsproto             1.2.0
```
####Tree:
```
.
├── poetry.lock
├── pyproject.toml
├── readme.md
├── src
│   ├── adapters
│   │   ├── __init__.py
│   │   ├── orm.py
│   │   └── repository.py
│   ├── config.py
│   ├── domain
│   │   ├── api_scraper.py
│   │   ├── chromedriver
│   │   ├── events.py
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── preprocessing.py
│   │   ├── schemas.py
│   │   └── scraper.py
│   ├── entrypoints
│   │   ├── __init__.py
│   │   └── my_app.py
│   ├── __init__.py
│   ├── page
│   │   └── templates
│   │       └── home.html
│   └── services_layer
│       ├── handlers.py
│       ├── __init__.py
│       ├── messagebus.py
│       └── unit_of_work.py
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── preprocessing_test.py
    ├── scraper_test.py
    ├── test_api.py
    ├── test_handlers.py
    ├── test_orm.py
    ├── test_repository.py
    └── test_uow.py
```
#####To crate this app we was used: 
Application architecture in Python
Harry Percival, Bob Gregory
#### run app
```$ uvicorn src.entrypoints.my_app:app --host 0.0.0.0 --port 5000```
#### send request to api to test it:
```$ curl http://localhost:5000/ping```
#### run scraper
```$ curl http://localhost:5000/fill_db```
#### get title from db
```$ curl http://localhost:5000/get_title/?title=[title]``` [title] searched title in subscription

