from collections.abc import Mapping
import os

from werkzeug import Request, Response

from dify_plugin import Endpoint


class NekoEndpoint(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        # read file from girls.html using current python file relative path
        path = values.get("path")
        if not path:
            return Response(
                "Path is required",
                status=400,
            )

        with open(os.path.join(os.path.dirname(__file__), path), "r") as f:
            return Response(
                f.read().replace("{{ bot_name }}", settings.get("bot_name", "Waifu")),
                status=200,
                content_type="text/html",
            )
