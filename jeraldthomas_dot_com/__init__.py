from flask import Flask

app = Flask(__name__)

from jeraldthomas_dot_com.analytics import *
import jeraldthomas_dot_com.views
