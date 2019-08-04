"""
This module is the Flask Blueprint for the homepage (/)
"""

from flask import Blueprint, render_template

homepage = Blueprint('homepage', __name__)


@homepage.route('/')
def display():
    """
    View function for displaying the homepage.
    Output: Rendered HTML page.
    """
    return render_template('home.html')
