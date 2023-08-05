from fastapi import APIRouter
from fastapi.responses import ORJSONResponse


class CBVRouter(APIRouter):
    registry = []

    def register(self, klass, prefix=None, tags=None):
        kls = klass()
        pth = prefix or '/{}/'.format(klass.__name__)

        for m in ['get', 'post', 'put', 'delete']:
            if hasattr(kls, m):
                self.add_api_route(pth, getattr(kls, m), response_class=ORJSONResponse, tags=tags, methods=[m.upper()])


router = CBVRouter()
