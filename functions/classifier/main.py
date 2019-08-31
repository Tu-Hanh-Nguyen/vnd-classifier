import tensorflow as tf
import numpy as np
import uuid
from flask import jsonify


from google.cloud import storage

import os

model = None
BUCKET = os.environ.get('GCS_BUCKET')
storage_client = storage.Client()

classes = ['1000', '10000', '100000', '2000', '20000', '200000', '5000', '50000', '500000']
FILENAME_TEMPLATE = '{}.jpg'

if not os.path.exists('/tmp/model'):
    os.makedirs('/tmp/model')
    
def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [192, 192])
    image /= 255.0  # normalize to [0,1] range

    return image

def download_blob(bucket_name, src_blob_name, dst_file_name):
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(src_blob_name)

    blob.download_to_filename(dst_file_name)

    print('Blob {} downloaded to {}.'.format(
        src_blob_name,
        dst_file_name))

def upload_blob(bucket_name, src_file, dst_file_name):
    """Upload a file to the bucket"""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob('uploaded/'+dst_file_name)

    blob.upload_from_string(src_file, content_type='image/jpg')

    print('File uploaded to uploaded/{}.'.format(dst_file_name))

def load_model():
    global model
    if not os.path.exists('/tmp/model/model.h5'):
        download_blob(BUCKET, 'model.h5', '/tmp/model/model.h5')

    path = '/tmp/model/model.h5'

    model = tf.keras.models.load_model(path)


def classifier(request):
    global model

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

    if model is None:
        load_model()

    file = request.files.get('filepond')
    if not file:
        return ("File not found", 400, headers)
    img_raw = file.read()

    img_preprocessed = preprocess_image(img_raw)
    outputs = model.predict(tf.expand_dims(img_preprocessed, 0))[0]
    pred_class = classes[np.argmax(outputs)]

    # upload file to storage
    id = uuid.uuid4().hex
    filename = FILENAME_TEMPLATE.format(id)
    upload_blob(BUCKET, img_raw, filename)

    return (jsonify([id, pred_class, [float(i) for i in outputs]]), 200, headers)