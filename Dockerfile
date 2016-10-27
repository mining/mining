FROM python:2.7

RUN apt-get update -y && apt-get install -y luajit luarocks nodejs npm build-essential

ADD ./requirements_dev.txt /app/requirements_dev.txt
WORKDIR /app
RUN wget https://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh
RUN bash Anaconda2-4.2.0-Linux-x86_64.sh -b -p /opt/conda
ENV PATH /opt/conda/bin:$PATH
RUN conda install anaconda-clean
RUN conda install pandas==0.17.1
RUN ["pip", "install", "Cython"]
RUN ["pip", "install", "numpy"]
RUN ["pip", "install", "-r", "requirements_dev.txt"]
RUN ["npm", "install", "-g", "bower"]
RUN ["ln", "-s", "/usr/bin/nodejs", "/usr/bin/node"]

ADD . /app
WORKDIR /app
RUN python --version
RUN ["python", "setup.py", "develop"]

RUN ["git", "submodule", "init"]
RUN ["git", "submodule", "update"]

WORKDIR /app/mining/frontend
RUN ["bower", "install", "--allow-root"]

WORKDIR /app
RUN cp mining/mining.docker.ini mining/mining.ini
CMD ["python", "manage.py", "runserver"]
