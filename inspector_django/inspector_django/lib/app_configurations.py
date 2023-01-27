from django.conf import settings


class GetFieldFromSettings:
    __defaults_configs = {
        'debug_settings': (
            'DEBUG',
            False
        ),
        'inspector_ingestion_key': (
            "INSPECTOR_INGESTION_KEY",
            None
        ),
        'curl_type': (
            "CURL_TYPE",
            "async",
        )
    }

    def get(self, field_name):
        try:
            attr = getattr(settings, self.__defaults_configs[field_name][0], self.__defaults_configs[field_name][1])
            return attr
        except:
            return None
