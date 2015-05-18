from flask import Flask
from web2lp import config

app = Flask(__name__)
app.config.from_object(config)

import web2lp.views
