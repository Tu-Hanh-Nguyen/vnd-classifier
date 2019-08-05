"""
This module is the Flask Blueprint for the classify API (/classify)
"""

from flask import Blueprint, redirect, url_for, request
from wand.image import Image

import uuid


classifier = Blueprint('classifier', __name__)


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

    data = file.read()
    with Image(blob=data) as image:
        converted_image = image.make_blob(format='jpg')

    id = uuid.uuid4().hex

    return (id, 200, headers)
