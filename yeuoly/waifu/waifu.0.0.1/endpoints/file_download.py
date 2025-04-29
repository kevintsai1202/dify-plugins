from collections.abc import Mapping
from werkzeug import Request, Response
from dify_plugin import Endpoint
from settings import Settings


class FileDownload(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        """
        Invokes the endpoint with the given request.
        """

        name = values.get("name")
        if not name:
            return Response("Name is required", status=400)
        
        try:
            settings_string = self.session.storage.get("__settings__").decode("utf-8")
        except Exception as e:
            settings_string = "{}"
        
        endpoint_settings = Settings.model_validate_json(settings_string) 

        # get settings from settings_mapping
        for background in endpoint_settings.backgrounds:
            if background.name == name:
                # read file from file_path
                file_bytes = self.session.storage.get(background.name)
                def generate():
                    for i in range(0, len(file_bytes), 4096):
                        yield file_bytes[i : i + 4096]
                
                return Response(generate(), content_type="application/octet-stream")
        
        return Response("Background not found", status=404)
