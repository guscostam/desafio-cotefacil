FROM python:3.10.4

ADD compra.py .

RUN pip install scrapy

WORKDIR /spiders

CMD [ "scrapy", "runspider", "compra.py"]