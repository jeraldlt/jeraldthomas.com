from functools import wraps
from flask import g, request, redirect, url_for
from tinydb import TinyDB
import time

def log_views(logfile):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            db = TinyDB(logfile)
            db.insert({'time': time.time(),
                      'endpoint': request.endpoint,
                      'ip': request.access_route,
                      'headers': dict(request.headers)})

            return f(*args, **kwargs)
        return decorated_function
    return decorator
