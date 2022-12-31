### Will be filed.
# run app
uvicorn src.entrypoints.my_app:app --host 0.0.0.0 --port 5000
# send request to api:
curl http://localhost:5000/ping 
