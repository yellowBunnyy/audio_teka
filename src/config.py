import os


def get_postgres_uri():
    return os.environ.get("DB_URI")

# def get_api_url():
#     host = "0.0.0.0"
#     port = 5000
#     return f"http://{host}:{port}"
