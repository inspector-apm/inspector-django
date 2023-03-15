from .lib import DjangoInspector
from .middleware import InspectorMiddleware
from .tracking import GuardTransaction
from django.core.handlers.wsgi import WSGIHandler
from .tracking import SQLHook
from .lib import GetFieldFromSettings
from .enums import SettingKeys


def sql_handler_wsgi(self, environ, start_response):
    request = self.request_class(environ)
    guard_transaction = GuardTransaction()
    if guard_transaction.check_monitoring_request_url(request):
        sql_hook = SQLHook(request)
        sql_hook.install_sql_hook()
    response = self.get_response(request)
    response._handler_class = self.__class__
    status = "%d %s" % (response.status_code, response.reason_phrase)
    response_headers = [
        *response.items(),
        *(("Set-Cookie", c.output(header="")) for c in response.cookies.values()),
    ]
    start_response(status, response_headers)
    return response


app_settings = GetFieldFromSettings()
monitoring_query_check = app_settings.get(SettingKeys.MONITORING_QUERY)
monitoring_request_check = app_settings.get(SettingKeys.MONITORING_REQUEST)
if monitoring_query_check and monitoring_request_check:
    WSGIHandler.__call__ = sql_handler_wsgi
