import json
from django.utils.encoding import force_str
import datetime
from django.db import connection

try:
    from psycopg2._json import Json as PostgresJson
    from psycopg2.extensions import STATUS_IN_TRANSACTION
except ImportError:
    PostgresJson = None
    STATUS_IN_TRANSACTION = None
try:
    from django.db.backends.utils import CursorWrapper
except ImportError:
    from django.db.backends.util import CursorWrapper
try:
    from django.db.backends import BaseDatabaseWrapper
except ImportError:
    from django.db.backends.base.base import BaseDatabaseWrapper


class SQLHook:
    _request: None
    NAME_CONTEXT_DB = 'DB'
    NAME_OBJ_CONTEXT_DB = 'query'
    CONNECTION_OBJ_CONTEXT_DB = 'connection'
    PARAMS_OBJ_CONTEXT_DB = 'bindings'

    def __init__(self, request):
        self._request = request

    def install_sql_hook(self):
        try:
            real_connect = BaseDatabaseWrapper.connect
        except AttributeError:
            return

        def _decode(param):
            if PostgresJson and isinstance(param, PostgresJson):
                return param.dumps(param.adapted)
            if isinstance(param, (tuple, list)):
                return [_decode(element) for element in param]
            if isinstance(param, dict):
                return {key: _decode(value) for key, value in param.items()}
            types_data = (datetime.datetime, datetime.date, datetime.time)
            try:
                return force_str(param, strings_only=not isinstance(param, types_data))
            except UnicodeDecodeError:
                return "(encoded string)"

        def __query_call_execute(method, sql, params):
            try:
                if self._request.inspector_middleware.can_add_segments():
                    nice_sql = sql.replace('"', '').replace(',', ', ')
                    type_segment = connection._connections._settings['default']['ENGINE']
                    self._request.inspector_middleware.start_segment(type_segment, nice_sql[0:50])
                    context = {
                        self.CONNECTION_OBJ_CONTEXT_DB: type_segment,
                        self.NAME_OBJ_CONTEXT_DB: nice_sql,
                        self.PARAMS_OBJ_CONTEXT_DB: params
                    }
                    self._request.inspector_middleware.segment().add_context(self.NAME_CONTEXT_DB, context)
                return method(sql, params)
            finally:
                if self._request.inspector_middleware.can_add_segments():
                    self._request.inspector_middleware.segment().end()
                    _params = ""
                    try:
                        _params = json.dumps(_decode(params))
                    except TypeError:
                        pass

        def callproc(self, procname, params=None):
            return __query_call_execute(self.cursor.callproc, procname, params)

        def execute(self, sql, params=None):
            return __query_call_execute(self.cursor.execute, sql, params)

        def executemany(self, sql, param_list):
            return __query_call_execute(self.cursor.executemany, sql, param_list)

        def connect(self):
            return real_connect(self)

        CursorWrapper.execute = execute
        CursorWrapper.executemany = executemany
        CursorWrapper.callproc = callproc
        BaseDatabaseWrapper.connect = connect
