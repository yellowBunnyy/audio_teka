FROM python:3.9

RUN mkdir -p /usr/my_app

WORKDIR /usr/my_app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# 
COPY ./requirements.txt /usr/my_app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /usr/my_app/requirements.txt

# 
COPY ./src /usr/my_app/src
COPY ./tests /usr/my_app/tests


