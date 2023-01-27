from inspector import Inspector, Configuration
from .app_configurations import GetFieldFromSettings


class DjangoInspector(Inspector):

    def __init__(self):
        app_settings = GetFieldFromSettings()
        ingestion_key = app_settings.get('inspector_ingestion_key')
        curl_type = app_settings.get('curl_type')
        configuration = Configuration(ingestion_key)
        configuration.set_transport(curl_type)
        super().__init__(configuration)
