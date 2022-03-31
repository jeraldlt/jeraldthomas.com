from functools import wraps
from flask import g, request, redirect, url_for
from tinydb import TinyDB
import time

def log_views(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = TinyDB('views.json')
        db.insert({'time': time.time(),
                  'endpoint': request.endpoint,
                  'ip': request.remote_addr})
        return f(*args, **kwargs)

    return decorated_function
