"""
This module is the Flask Blueprint for the classify API (/classify)
"""

from flask import Blueprint, redirect, url_for, request, jsonify

# from helpers import image_catalog
# from google.cloud import firestore
# from google.cloud import storage

import os
import time

import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers

from io import BytesIO
import numpy as np

import uuid


classifier = Blueprint('classifier', __name__)
path = 'static/model/'
model = tf.keras.experimental.load_from_saved_model(
    path, custom_objects={'KerasLayer': hub.KerasLayer})
classes = [5000, 10000]

# BUCKET = os.environ.get('GCS_BUCKET')
FILENAME_TEMPLATE = '{}.jpg'
# client = storage.Client()


def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [224, 224])
    image /= 255.0  # normalize to [0,1] range

    return image


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
    img_raw = file.read()
    open(os.path.join('uploads/', FILENAME_TEMPLATE.format(file.filename)),
         'wb').write(img_raw)

    # img = open_image(file.read())
    # with Image(blob=data) as image:
    #     converted_image = image.make_blob(format='jpg')

    id = uuid.uuid4().hex

    # Integrate with Firebase
    # filename = FILENAME_TEMPLATE.format(id)
    # bucket = client.get_bucket(BUCKET)
    # blob = bucket.blob(filename)
    # blob.upload_from_string(converted_image, content_type='image/jpg')

    # image = image_catalog.Image(user_confirmed='',
    #                             image_url=filename,
    #                             label='',
    #                             created_at=int(time.time()))
    # image_id = image_catalog.add_image(image)

    img_preprocessed = preprocess_image(img_raw)
    outputs = model.predict(tf.expand_dims(img_preprocessed, 0))[0]
    pred_class = classes[np.argmax(outputs)]

    return (jsonify([id, str(pred_class), [float(i) for i in outputs]]), 200, headers)
