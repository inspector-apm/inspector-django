from .lib import GetFieldFromSettings, DjangoInspector
from .enums import SettingKeys
from django.utils.deprecation import MiddlewareMixin
from .tracking import GuardTransaction


class InspectorMiddleware(MiddlewareMixin):
    TYPE_TRANSACTION = 'request'
    NAME_CONTEXT_DB = 'DB'
    NAME_OBJ_CONTEXT_DB = 'query'
    __key_status_code = 'status_code'

    get_response = None
    monitoring_request_check = None
    guard_transaction: GuardTransaction = None

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response
        self.guard_transaction = GuardTransaction()
        app_settings = GetFieldFromSettings()
        self.monitoring_request_check = app_settings.get(SettingKeys.MONITORING_REQUEST)

    def process_request(self, request):
        request.inspector = DjangoInspector()
        request.inspector_middleware = DjangoInspector()
        if self.monitoring_request_check and self.guard_transaction.check_monitoring_request_url(
                request) and self.should_recorded:
            name_transaction = request.inspector_middleware.get_name_transaction(request)
            request.inspector_middleware.start_transaction(name_transaction, self.TYPE_TRANSACTION)

    def process_response(self, request, response):
        if self.monitoring_request_check and self.guard_transaction.check_monitoring_request_url(
                request) and self.should_recorded:
            request.inspector_middleware.set_http_request(request)
            request.inspector_middleware.add_context_response(response)
            status_code = getattr(response, self.__key_status_code, None)
            request.inspector_middleware.transaction().set_result(status_code)
            del request.inspector_middleware
        return response

    def process_exception(self, request, exception):
        if self.monitoring_request_check:
            request.inspector_middleware.report_exception(exception, True, True)

    def should_recorded(self, request):
        return True
