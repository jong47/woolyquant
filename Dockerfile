FROM python:3.11.4

WORKDIR /src

COPY requirements.txt ./

RUN npm install -r 
RUN python -m pip install -r
RUN pip install iexfinance -r 
RUN pip install pandas -r

COPY src/* ./

CMD [ "", "" ]