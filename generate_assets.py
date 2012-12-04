#!/usr/bin/python

import os
import sys
from paste.deploy.loadwsgi import appconfig
from skylines.config.environment import load_environment
from skylines.lib.assets import Environment

sys.path.append(os.path.dirname(sys.argv[0]))

conf_path = '/etc/skylines/production.ini'
if len(sys.argv) > 1:
    conf_path = sys.argv[1]
conf = appconfig('config:' + os.path.abspath(conf_path))
load_environment(conf.global_conf, conf.local_conf)

env = Environment(conf)

bundles_path = os.path.join(os.path.dirname(sys.argv[0]), 'assets', 'bundles.yaml')
env.load_bundles(bundles_path)

for bundle in env:
    bundle.build()
