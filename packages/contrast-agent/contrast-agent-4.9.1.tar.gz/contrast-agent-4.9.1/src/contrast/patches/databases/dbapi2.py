# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Implements a single API for instrumenting all dbapi2-compliant modules
"""
from contrast.agent.policy import patch_manager
from contrast.applies.sqli import apply_rule
from contrast.utils.decorators import fail_safely
from contrast.utils.patch_utils import patch_cls_or_instance


def _build_patch(database, action):
    def patched_method(orig_func, patch_policy, *args, **kwargs):
        return apply_rule(database, action, orig_func, args, kwargs)

    return patched_method


def _instrument_cursor_method(database, cursor, method_name):
    new_method = _build_patch(database, method_name)
    patch_cls_or_instance(cursor, method_name, new_method)
    func = patch_manager.as_func(getattr(cursor, method_name))
    func.__name__ = method_name


def instrument_cursor(database, cursor):
    """
    Instruments a dbapi2-compliant database cursor class

    @param database: Name of the database module being patched (e.g. "sqlite3")
    @param cursor: Reference to cursor class to be instrumented
    """
    _instrument_cursor_method(database, cursor, "execute")
    _instrument_cursor_method(database, cursor, "executemany")


def instrument_executescript(database, cursor):
    """
    Instruments the `executescript` method of a database cursor class

    The executescript method is non-standard but is provided by some drivers
    including sqlite3.

    @param database: Name of the database module being patched (e.g. "sqlite3")
    @param cursor: Reference to cursor class to be instrumented
    """
    _instrument_cursor_method(database, cursor, "executescript")


@fail_safely("failed to instrument database adapter")
def instrument_adapter(database, adapter):
    """
    In some cases (SQLAlchemy), we need to instrument an unknown PEP-249 compliant
    adapter. We only have a reference to the adapter module, and we can't make any
    assumptions about the existence of `adapter.Cursor`, since this is not guaranteed
    by the spec.

    We are only guaranteed the following:
    - the adapter has a `connection()` method, which returns an instance of Connection
    - the Connection object has a `cursor()` method, which returns an instance of Cursor
    - the Cursor has `execute()` and `executemany()` methods

    This requires a somewhat roundabout instrumentation strategy:
    - on the first call to adapter.connect(), we can access the Connection class
    - on the first call to Connection.cursor(), we can access the Cursor class
    - this lets us instrument Cursor.execute() and Cursor.executemany()
    """

    @fail_safely("failed to instrument database cursor object")
    def safe_instrument_cursor(cursor_instance):
        """
        Safely instrument a Cursor class given an instance of that class
        """
        cursor_class = type(cursor_instance)
        if not patch_manager.is_patched(cursor_class.execute):
            instrument_cursor(database, cursor_class)

    @fail_safely("failed to instrument database connection object")
    def safe_instrument_connection(connection_instance):
        """
        Safely instrument a Connection class given an instance of that class
        """
        connection_class = type(connection_instance)
        if not patch_manager.is_patched(connection_class.cursor):
            patch_cls_or_instance(connection_class, "cursor", cursor_patch)

    def cursor_patch(orig_func, _, *args, **kwargs):
        """
        Patch for dbapi_adapter.connection().cursor()

        This patch will ensure that the returned Cursor object's class will have
        `execute` and `executemany` instrumented.
        """
        cursor = orig_func(*args, **kwargs)
        safe_instrument_cursor(cursor)
        return cursor

    def connect_patch(orig_func, _, *args, **kwargs):
        """
        Patch for dbapi_adapter.connection()

        This patch will ensure that the returned Connection object's class will have
        `cursor_patch` applied to its cursor() method.
        """
        connection = orig_func(*args, **kwargs)
        safe_instrument_connection(connection)
        return connection

    if not patch_manager.is_patched(adapter.connect):
        patch_cls_or_instance(adapter, "connect", connect_patch)
