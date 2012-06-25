# SkyLines - example configuration
DEBUG = True
SECRET_KEY = '4090eda8-6d94-4d32-9c94-833e075a43f0'

SQLALCHEMY_DATABASE_URI = 'postgres:///skylines'

SKYLINES = {
    'imprint_link': '/imprint',
    'analysis': {
        'path': '/opt/skylines/bin',
    },
    'files': {
        'path': './htdocs/files',
        'uri': '/files',
    },
    'static': {
        'jquery': '/js/jQuery/',
        'fontawesome': 'http://fortawesome.github.com/Font-Awesome/assets/',
        'bootstrap': 'http://twitter.github.com/bootstrap/assets/',
    },
    'lists': {
        'display_length': 50,
        'server_side': 250,
    },
}
