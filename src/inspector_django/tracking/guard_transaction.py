from ..lib.app_configurations import GetFieldFromSettings
from django.urls import resolve
from ..enums import SettingKeys
import fnmatch, re


class GuardTransaction:
    app_settings = None
    __expr = "/([.*+?^=!:$<>()|\[\]\/\\])/g"
    __expr_replace = "\\$1"

    def __init__(self):
        self.app_settings = GetFieldFromSettings()

    def check_monitoring_request_url(self, request_data):
        list_ignore_url = self.app_settings.get(SettingKeys.INSPECTOR_IGNORE_URL)
        try:
            current_route_url = resolve(request_data.path_info)
            current_url = current_route_url.route
        except Exception as e:
            current_url = request_data.path_info
        if current_url in list_ignore_url:
            return False
        for item_ignore_url in list_ignore_url:
            array_ignore_url = item_ignore_url.split('*')
            for idx, item_segment_url in enumerate(array_ignore_url):
                array_ignore_url[idx] = re.sub(self.__expr_replace, self.__expr_replace, item_segment_url)
            str_role_replaced = '^' + '.*'.join(array_ignore_url) + '$'
            res_match = re.compile(str_role_replaced).match(current_url)
            if res_match:
                return False
        return True
