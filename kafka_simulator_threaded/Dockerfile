FROM python:3.7.2-alpine3.7

WORKDIR /app

ADD app.py /app/.
ADD params.py /app/.
ADD requirements.txt /app/.

RUN pip install -r requirements.txt

#EXPOSE 80

CMD ["python", "app.py"]

#ZEND
