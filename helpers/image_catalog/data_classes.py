"""
Data class for images.
"""


from dataclasses import dataclass
from typing import List


@dataclass
class Image:
    """
    Data class for images.
    """
    image_url: str
    label: str
    user_confirmed: str
    created_at: int
    id: str = None

    @staticmethod
    def deserialize(document):
        """
        Helper function for parsing a Firestore document to a Image object.

        Parameters:
           document (DocumentSnapshot): A snapshot of Firestore document.

        Output:
           A Image object.
        """
        data = document.to_dict()
        if data:
            return Image(
                id=document.id,
                image_url=data.get('image_url'),
                label=data.get('label'),
                user_confirmed=data.get('user_confirmed'),
                created_at=data.get('created_at')
            )

        return None
