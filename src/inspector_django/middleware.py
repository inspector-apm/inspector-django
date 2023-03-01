from django.db import connection
import os
from .lib import GetFieldFromSettings, DjangoInspector
from .enums import SettingKeys
from django.utils.deprecation import MiddlewareMixin

"""
 DA ELIMINARE
"""


def terminal_width():
    """
    Function to compute the terminal width.
    """
    width = 0
    try:
        import struct, fcntl, termios
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
        width = struct.unpack('HHHH', x)[1]
    except:
        pass
    if width <= 0:
        try:
            width = int(os.environ['COLUMNS'])
        except:
            pass
    if width <= 0:
        width = 80
    return width


def print_terminal(query):
    indentation = 2
    width = terminal_width()
    nice_sql = query['sql'].replace('"', '').replace(',', ', ')
    sql = "\033[1;31m[%s]\033[0m %s" % (query['time'], nice_sql)
    while len(sql) > width - indentation:
        print("%s%s" % (" " * indentation, sql[:width - indentation]))
        sql = sql[width - indentation:]
    print("%s%s\n" % (" " * indentation, sql))


def SqlPrintingMiddleware(get_response):
    def middleware(request):
        request.my_var = "test variabile"
        response = get_response(request)

        # if not settings.DEBUG or len(connection.queries) == 0 or request.path_info.startswith(settings.MEDIA_URL) or  '/admin/jsi18n/' in request.path_info:
        #    return response
        app_settings = GetFieldFromSettings()
        monitoring_query_check = app_settings.get(SettingKeys.MONITORING_QUERY)
        # print('monitoring_query_check: ', monitoring_query_check)

        indentation = 2
        # print("\n\n%s\033[1;35m[SQL Queries for]\033[1;34m %s\033[0m\n" % (" " * indentation, request.path_info))
        total_time = 0.0
        for query in connection.queries:
            print_terminal(query)
        replace_tuple = (" " * indentation, str(total_time))
        # print("%s\033[1;32m[TOTAL TIME: %s seconds]\033[0m" % replace_tuple)
        # print("%s\033[1;32m[TOTAL QUERIES: %s]\033[0m" % (" " * indentation, len(connection.queries)))
        return response

    return middleware


"""
 END DA ELIMINARE
"""


class InspectorMiddleware(MiddlewareMixin):
    TYPE_TRANSACTION = 'request'
    NAME_CONTEXT_DB = 'DB'
    NAME_OBJ_CONTEXT_DB = 'query'

    # INSPECTOR FOR MIDDLEWARE
    middleware_inspector = None
    get_response = None

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response
        self.middleware_inspector = DjangoInspector()
    """
    def __call__(self, request):
        request.inspector = DjangoInspector()
        request.inspector_middleware = DjangoInspector()
        method_request = request.method
        path_request = request.path_info
        name_transaction = "{} {}".format(method_request, path_request)
        request.inspector_middleware.start_transaction(name_transaction, self.TYPE_TRANSACTION)
        response = self.get_response(request)
        request.inspector_middleware.set_name_transaction(request)
        request.inspector_middleware.set_http_request(request)
        request.inspector_middleware.add_context_response(response)
        status_code = getattr(response, 'status_code', None)
        request.inspector_middleware.set_status_response(status_code)
        del request.inspector_middleware
        return response
    """
    def process_request(self, request):
        request.inspector = DjangoInspector()
        request.inspector_middleware = DjangoInspector()
        method_request = request.method
        path_request = request.path_info
        name_transaction = "{} {}".format(method_request, path_request)
        request.inspector_middleware.start_transaction(name_transaction, self.TYPE_TRANSACTION)

    def process_response(self, request, response):
        request.inspector_middleware.set_name_transaction(request)
        request.inspector_middleware.set_http_request(request)
        request.inspector_middleware.add_context_response(response)
        status_code = getattr(response, 'status_code', None)
        request.inspector_middleware.set_status_response(status_code)
        del request.inspector_middleware
        return response

    def process_exception(self, request, exception):
        pass

    """
    def process_request(self, request):
        request.inspector = DjangoInspector()
        request.inspector_middleware = DjangoInspector()
        method_request = request.method
        path_request = request.path_info

        name_transaction = "{} {}".format(method_request, path_request)
        # print('name_transaction: ', name_transaction)
        request.inspector_middleware.start_transaction(name_transaction, self.TYPE_TRANSACTION)
        sql_hook = SQLHook(request)
        sql_hook.install_sql_hook()

    def process_response(self, request, response):
        app_settings = GetFieldFromSettings()

        # for item_connection in connections.all():
        #    wrapper_obj = wrap_cursor(item_connection)

        monitoring_query_check = app_settings.get(SettingKeys.MONITORING_QUERY)
        monitoring_request_check = app_settings.get(SettingKeys.MONITORING_REQUEST)

        request.inspector_middleware.set_name_transaction(request)
        request.inspector_middleware.set_http_request(request)
        request.inspector_middleware.add_context_response(response)

        # print('\n\n ---> request', request.environ['SERVER_PROTOCOL'],'\n\n')
        # print('\n\n ---> response', response.__dict__, '\n\n')
        
        if monitoring_query_check:  
            total_time = 0
            # print('connection: ', connection._connections.__dict__)
            for query in connection.queries:
                # print_terminal(query)
                nice_sql = query['sql'].replace('"', '').replace(',', ', ')
                type_segment = connection._connections._settings['default']['ENGINE']
                request.inspector_middleware.start_segment(type_segment, nice_sql[0:50])
                context = {}
                context[self.NAME_OBJ_CONTEXT_DB] = nice_sql
                request.inspector_middleware.segment().add_context(self.NAME_CONTEXT_DB, context)
                time_query = float(query['time'])
                request.inspector_middleware.segment().end(time_query)
                # print('time_query: ', round(time_query, 4))
                # print('query __dict__: ', query)
                # print('TIME END STR: ', time_query)

        # print('method: ', request.method)
        # print('method: ', request.__dict__)
        
        del request.inspector_middleware
        return response

"""
