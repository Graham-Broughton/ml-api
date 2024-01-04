# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api, Resource, reqparse
import werkzeug
import PIL
from io import BytesIO
from fastai.vision import load_learner
from fastai.vision.image import pil2tensor
import fastai
from pathlib import Path
import numpy as np
import os
import requests

MODEL_PATH = Path("./models")
# =============================================================================
# DATA_PATH = Path("../images/320") # local
# =============================================================================
DATA_PATH = Path("/images/mo/960") # server
app = Flask(__name__)
api = Api(app)

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
    response.headers.add("Access-Control-Allow-Methods", "POST")
    return response

learn = load_learner(MODEL_PATH, "resnet34_min100figs_vote1_5.pkl")

class predict(Resource):

    def get(self):
        pass

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument("file", type=werkzeug.datastructures.FileStorage,
                           location="files")
        parse.add_argument("id", type=int)
        args = parse.parse_args()
        image = args["file"]
        id_ = args["id"]
        if image is None:
            if os.path.exists(DATA_PATH / f"{id_}.jpg"):
                image = PIL.Image.open(DATA_PATH / f"{id_}.jpg")
            else:
                url = f"https://images.mushroomobserver.org/960/{id_}.jpg"
                response = requests.get(url)
                print(url)
                image = PIL.Image.open(BytesIO(response.content))
        else:
            image = image.read()
            image = PIL.Image.open(BytesIO(image))
        image = pil2tensor(image.convert("RGB"), np.float32).div_(255)
        image = fastai.vision.image.Image(image)
        _, _, ten = learn.predict(image.resize(300))
        return [(learn.data.classes[idx], float(prob) * 100)
                for idx, prob in zip(ten.topk(5).indices, ten.topk(5).values)]

api.add_resource(predict, "/predict")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
