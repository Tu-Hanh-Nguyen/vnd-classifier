"""
A collection of helper functions for image related operations.
"""

from dataclasses import asdict
import os
import uuid

from google.cloud import firestore

from .data_classes import Image

BUCKET = os.environ.get('GCS_BUCKET')

firestore_client = firestore.Client()


def add_image(image):
    """
    Helper function for adding a image.

    Parameters:
       image (Image): A Image object.

    Output:
       The ID of the image.
    """

    image_id = uuid.uuid4().hex
    firestore_client.collection('images').document(
        image_id).set(asdict(image))
    return image_id


def get_image(image_id):
    """
    Helper function for getting a image.

    Parameters:
       image_id (str): The ID of the image.

    Output:
       A Image object.
    """

    image = firestore_client.collection(
        'images').document(image_id).get()
    return Image.deserialize(image)


def list_images():
    """
    Helper function for listing images.

    Parameters:
       None.

    Output:
       A list of Image objects.
    """

    images = firestore_client.collection(
        'images').order_by('created_at').get()
    image_list = [Image.deserialize(image) for image in list(images)]
    return image_list
