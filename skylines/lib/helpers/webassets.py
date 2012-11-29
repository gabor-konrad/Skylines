from __future__ import absolute_import
from tg import config
from webassets import Environment, Bundle

__all__ = ['get_env', 'bundle']


def get_env():
    if 'asset_env' not in config:
        config['asset_env'] = Environment('skylines/public/gen', '/gen',
                                          load_path=['skylines/public'])

    return config['asset_env']


def bundle(*contents, **options):
    # Get the Environment
    env = get_env()

    # Create the Bundle
    bundle_name = ', '.join(contents)
    _bundle = Bundle(*contents, **options)

    # Register the Bundle with the Environment
    if bundle_name not in env:
        env.register(bundle_name, _bundle)

    # Return the output file(s)
    return env[bundle_name].urls()
