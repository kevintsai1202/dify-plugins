from typing import Mapping
from werkzeug import Request, Response
from dify_plugin import Endpoint
from settings import Background, Settings

class FileUpload(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        name = values.get("name")
        if not name:
            return Response("Name is required", status=400)
        
        file = r.files.get("file")
        if not file:
            return Response("File is required", status=400)
        
        try:
            settings_string = self.session.storage.get("__settings__").decode("utf-8")
        except Exception as e:
            settings_string = "{}"
        
        endpoint_settings = Settings.model_validate_json(settings_string) 

        # add to endpoint_settings.backgrounds if not exists
        if not any(background.name == name for background in endpoint_settings.backgrounds):
            endpoint_settings.backgrounds.append(Background(name=name))
        
        self.session.storage.set("__settings__", endpoint_settings.model_dump_json().encode("utf-8"))
        self.session.storage.set(name, file.read())
        
        return Response("File uploaded", status=200)
