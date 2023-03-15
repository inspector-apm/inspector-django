from dataclasses import dataclass


@dataclass
class SettingKeys:
    INGESTION_KEY = 'inspector_ingestion_key'
    INSPECTOR_TRANSPORT = 'inspector_transport'
    MONITORING_QUERY = 'inspector_monitoring_query'
    MONITORING_REQUEST = 'inspector_monitoring_request'
    INSPECTOR_IGNORE_URL = 'inspector_ignore_url'
