from collections.abc import Mapping

from werkzeug import Request, Response

from dify_plugin import Endpoint


class NekoEndpoint(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        # read file from girls.html using current python file relative path
        return Response(
            "Redirecting to /asset/index.html",
            status=302,
            headers={"Location": "/asset/index.html"},
        )
