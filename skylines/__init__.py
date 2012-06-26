from flask import Flask
from sqlalchemy import create_engine
from skylines.model import init_model

app = Flask(__name__)
app.config.from_object('skylines.default_settings')
app.config.from_envvar('SKYLINES_SETTINGS', silent=True)

init_model(create_engine(app.config['SQLALCHEMY_DATABASE_URI']))

import skylines.views
