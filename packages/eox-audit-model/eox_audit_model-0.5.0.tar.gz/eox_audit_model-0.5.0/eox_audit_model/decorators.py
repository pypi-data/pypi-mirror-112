"""eox-audit-model decorators file.

Functions:
    audit_method: audit decorator.
"""
from functools import wraps

from eox_audit_model.models import AuditModel


def audit_method(action='Undefined action.'):
    """Decorator in order to audit methods.

    Arguments:
        action: String, action associated to the audit process.

    Return:
        decorator output.
    """
    def decorator(func):
        """Decorator function"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Set the parameter in the right format and call AuditModel.execute_action"""
            parameters = {
                'args': args,
                'kwargs': kwargs,
            }

            return AuditModel.execute_action(
                action=action,
                method=func,
                parameters=parameters,
            )

        return wrapper

    return decorator


def rename_function(name=''):
    """Change the __name__ atribute of a function to the given name parameter if any.
    This allows to provide a more descriptive method name than `api_method`.
    """
    def decorator(func):
        """Decorator function"""
        if name:
            func.__name__ = name
        return func
    return decorator


def audit_drf_api(action='', data_filter=None, hidden_fields=None, method_name='api_method'):
    """This decorator wraps the functionality of audit_method in order to
    work with django API view methods,also this allows to filter the data that will be
    stored in the data base.

    Example

    class YourAPIView(APIView):

        @audit_api_wrapper(action='Get my items', data_filter=['username', 'location'])
        def get(self, request, *args, **kwargs):
            ...
    """
    def decorator(func):  # pylint: disable=missing-docstring
        @wraps(func)
        def wrapper(*args, **kwargs):  # pylint: disable=missing-docstring
            request = args[1]
            data = request.data if request.data else request.query_params

            audit_data = {
                key: value
                for key, value in data.items()
                if data_filter and key in data_filter
            }
            audit_data.update(
                {key: '*****' for key in data if hidden_fields and key in hidden_fields}
            )

            @audit_method(action=action)
            @rename_function(name=method_name)
            def api_method(audit_data):  # pylint: disable=unused-argument
                """This method is just a wrapper in order to capture the input data"""
                return func(*args, **kwargs)

            return api_method(audit_data)

        return wrapper

    return decorator
