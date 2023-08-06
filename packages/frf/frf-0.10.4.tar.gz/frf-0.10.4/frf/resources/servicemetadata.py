"""Declares :class:`ServiceMetadataResource`."""
from fastapi import Request
from fastapi.responses import Response

from ..dependency import Injected
from ..views import AnonymousResource


class ServiceMetadataResource(AnonymousResource):
    resource_name = "Metadata"

    async def list(self,
        request: Request,
        response: Response,
        svc=Injected('APIMetadataService')
    ):
        """Return a JSON object describing all API properties."""
        response.headers['Access-Control-Allow-Origin'] = '*'
        return await svc.get(self.asgi, request)
