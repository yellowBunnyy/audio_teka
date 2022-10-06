import os


def get_postgres_uri():
    host = os.environ.get("MY_DB_HOST")
    port = 5432
    password = os.environ.get("MY_DB_PASS")
    user = os.environ.get("DB_USER_NAME")
    db_name = "audio"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = "localhost"
    port = 5000
    return f"http://{host}:{port}"
