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
        'inspector_transport': (
            "INSPECTOR_TRANSPORT",
            "async",
        ),
        'inspector_monitoring_query': (
            "INSPECTOR_MONITORING_QUERY",
            True,
        ),
        'inspector_monitoring_request': (
            "INSPECTOR_MONITORING_REQUEST",
            True,
        ),
        'inspector_ignore_url': (
            "INSPECTOR_IGNORE_URL",
            [
                'static*',
                'media*'
                'assets*',
                'js*',
                'css*',
            ],
        )
    }

    def get(self, field_name):
        try:
            attr = getattr(settings, self.__defaults_configs[field_name][0], self.__defaults_configs[field_name][1])
            return attr
        except:
            return None
