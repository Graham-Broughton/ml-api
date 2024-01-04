FROM python:3.7

COPY . /mushroom_api
WORKDIR /mushroom_api

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "api.py"]
