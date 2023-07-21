FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends --quiet python3 python3-pip python3-dev python3-numpy pybind11-dev cmake git g++ \
    && apt-get clean all

WORKDIR /app

COPY . /app

RUN mkdir -p /app/res/data

COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Build the shared object file
RUN g++ -O2 -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` ./src/stock_pair.cc -o ./src/stock_pair.so
RUN git submodule update --init
RUN cmake 

CMD [ "python3", "./src/smart_pair.py" ]