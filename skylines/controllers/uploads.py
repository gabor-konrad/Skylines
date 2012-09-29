from tg import expose, redirect, request
from tg.decorators import with_trailing_slash
from webob.exc import HTTPUnauthorized, HTTPBadRequest

from skylines.lib.base import BaseController
from skylines.model.session import DBSession
from skylines.model.igcfile import IGCFile


def parse_non_negative_integer(value):
    try:
        value = int(value)
    except ValueError:
        raise HTTPBadRequest

    if value < 0:
        raise HTTPBadRequest

    return value


class paginate:
    def __init__(self, query_key):
        self.query_key = query_key

    def __call__(self, func):
        def apply_pagination(*remainder, **kw):
            original = func(*remainder, **kw)

            if self.query_key not in original:
                return original

            if 'limit' in kw:
                original[self.query_key] = original[self.query_key].limit(parse_non_negative_integer(kw['limit']))

            if 'offset' in kw:
                original[self.query_key] = original[self.query_key].offset(parse_non_negative_integer(kw['offset']))

            original[self.query_key] = original[self.query_key].all()

            return original

        return apply_pagination


class IGCUploadsController(BaseController):
    @with_trailing_slash
    @expose('json')
    @paginate('files')
    def index(self, **kw):
        if not request.identity:
            raise HTTPUnauthorized()

        def to_criteria(model, str):
            criteria = []
            for token in str.split(','):
                field = token.lstrip('-')
                try:
                    criterion = getattr(model, field)
                except AttributeError:
                    raise HTTPBadRequest

                if token.startswith('-'):
                    criterion = criterion.desc()

                criteria.append(criterion)

            return criteria

        query = DBSession.query(IGCFile).filter(IGCFile.owner == request.identity['user'])

        if 'order_by' in kw:
            order_by = to_criteria(IGCFile, kw['order_by'])
            query = query.order_by(*order_by)

        return dict(files=query)


class UploadsController(BaseController):
    igc = IGCUploadsController()

    @with_trailing_slash
    @expose()
    def index(self, **kw):
        redirect('igc/')
