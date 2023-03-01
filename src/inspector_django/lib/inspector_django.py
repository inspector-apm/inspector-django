from inspector import Inspector, Configuration
from .app_configurations import GetFieldFromSettings
from ..enums import SettingKeys
from inspector.models.partials import HTTP, URL
import json
from datetime import datetime
import time


class DjangoInspector(Inspector):
    NAME_RESPONSE_CONTEXT = 'response'

    def __init__(self):
        app_settings = GetFieldFromSettings()
        ingestion_key = app_settings.get(SettingKeys.INGESTION_KEY)
        curl_type = app_settings.get(SettingKeys.INSPECTOR_TRANSPORT)
        configuration = Configuration(ingestion_key)
        configuration.set_transport(curl_type)
        super().__init__(configuration)

    def __del__(self):
        super().__del__()

    def set_name_transaction(self, request_data):
        if request_data.resolver_match is not None:
            name_transaction = "{} {}".format(request_data.method, request_data.resolver_match.route)
            self.transaction().name = name_transaction

    def set_http_request(self, request_data):
        http = HTTP()
        request_transaction = self.__get_request_transaction(request_data)
        http.set_request(request_transaction)
        url = URL()
        url.set_path(request_data.path_info)
        url.set_port(int(request_data.environ['SERVER_PORT']))
        url.set_search(request_data.environ['QUERY_STRING'])
        url.set_protocol(request_data.scheme)
        url.set_full(request_data.build_absolute_uri())
        http.set_url(url)
        self.transaction().set_http(http)

    def set_status_response(self, code):
        status_response = None
        if code == 200 or code == 201:
            status_response = 'success'
        self.transaction().set_result(status_response)
        return status_response

    def __get_request_transaction(self, request_data):
        request_transaction = {
            "method": request_data.method,
            "version": request_data.environ['SERVER_PROTOCOL'],
            "socket": {
                "remote_address": request_data.environ['REMOTE_ADDR'],
                "encrypted": False
            },
            "cookies": request_data.COOKIES,
            "headers": request_data.headers
        }
        return request_transaction

    def add_context_response(self, response_data):
        context_data = {
            'response': {
                'template_name': response_data['template_name'] if 'template_name' in response_data else None,
                'headers': response_data.headers,
                'cookies': response_data.cookies
            }
        }
        self.transaction().add_context(self.NAME_RESPONSE_CONTEXT, context_data)
