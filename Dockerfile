FROM debian:buster-slim

RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends --quiet python3 python3-venv libpq-dev python3-dev python3-pip pybind11-dev cmake git g++ python3-psycopg2 \
    && apt-get clean all

RUN pip3 install --upgrade pip

COPY . /app
COPY requirements.txt ./

RUN mkdir -p /app/res/data/pairs
RUN mkdir -p /app/res/data/stocks

WORKDIR /app
RUN pip3 cache purge
RUN pip3 install --no-cache-dir -r requirements.txt

# Build the shared object file
RUN g++ -O2 -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` ./src/stock_pair.cc -o ./src/stock_pair.so
# RUN git submodule update --init
RUN cmake 

CMD [ "python3", "./src/cria.py" ]