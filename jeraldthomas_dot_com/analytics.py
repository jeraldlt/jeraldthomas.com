from functools import wraps
from flask import g, request, redirect, url_for

def log_views(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Logging:", request.url)
        return f(args, kwargs)
        
    return decorated_function
