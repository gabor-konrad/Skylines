import webassets
from webassets.loaders import YAMLLoader
from paste.deploy.converters import asbool


class Environment(webassets.Environment):
    def __init__(self, config):
        super(Environment, self).__init__(config['webassets.base_dir'],
                                          config['webassets.base_url'],
                                          debug=asbool(config.get('webassets.debug', False)),
                                          auto_build=asbool(config.get('webassets.auto_build', False)))

    def load_bundles(self, bundle_file):
        loader = YAMLLoader(bundle_file)
        bundles = loader.load_bundles()
        self.register(bundles)
