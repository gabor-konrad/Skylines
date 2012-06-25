from flask import Flask

app = Flask(__name__)
app.config.from_object('skylines.default_settings')
app.config.from_envvar('SKYLINES_SETTINGS', silent=True)

import skylines.views
