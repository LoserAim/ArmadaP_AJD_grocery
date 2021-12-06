from flask import Blueprint

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'