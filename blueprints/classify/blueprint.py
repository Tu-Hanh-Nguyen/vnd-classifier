"""
This module is the Flask Blueprint for the classify API (/classify)
"""

from flask import Blueprint, redirect, url_for, request, jsonify
from wand.image import Image
from fastai.vision import *
from io import BytesIO

import uuid


classifier = Blueprint('classifier', __name__)

learner = load_learner('static/model/')


@classifier.route('/classify', methods=['POST'])
def process():
    # Set up CORS to allow requests from arbitrary origins.
    # See https://cloud.google.com/functions/docs/writing/http#handling_cors_requests
    # for more information.
    # For maxiumum security, set Access-Control-Allow-Origin to the domain
    # of your own.
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    file = request.files.get('filepond')
    if not file:
        return ("File not found", 400, headers)

    # img = open_image(file.read())
    # with Image(blob=data) as image:
    #     converted_image = image.make_blob(format='jpg')

    img = open_image(BytesIO(file.read()))

    id = uuid.uuid4().hex

    pred_class, pred_idx, outputs = learner.predict(img)

    return (jsonify([id, str(pred_class), [float(i) for i in outputs]]), 200, headers)
