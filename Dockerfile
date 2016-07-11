FROM python:2.7

RUN apt-get update -y && apt-get install -y luajit luarocks nodejs npm build-essential

ADD ./requirements_dev.txt /app/requirements_dev.txt
WORKDIR /app
RUN ["pip", "install", "Cython"]
RUN ["pip", "install", "numpy"]
RUN ["pip", "install", "-r", "requirements_dev.txt"]
RUN ["npm", "install", "-g", "bower"]
RUN ["ln", "-s", "/usr/bin/nodejs", "/usr/bin/node"]

ADD . /app
WORKDIR /app
RUN ["python", "setup.py", "develop"]

RUN ["git", "submodule", "init"]
RUN ["git", "submodule", "update"]

WORKDIR /app/mining/frontend
RUN ["bower", "install", "--allow-root"]

WORKDIR /app
CMD ["python", "manage.py", "runserver"]
