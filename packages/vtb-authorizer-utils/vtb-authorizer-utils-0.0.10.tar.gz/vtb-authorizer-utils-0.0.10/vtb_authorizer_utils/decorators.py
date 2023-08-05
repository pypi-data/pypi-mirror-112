from typing import Set, Optional

from vtb_authorizer_utils.authorizer_schema_builder import ContextType, AuthorizerSchemaBuilder


def authorizer_resource_type(service: str,
                             name: str,
                             title: Optional[str] = None,
                             description: Optional[str] = None):
    """ Добавление описания ресурсного типа """

    def decorator(view_class):
        AuthorizerSchemaBuilder().add_resource_type(service, name, view_class.__qualname__, title, description)
        return view_class

    return decorator


def authorizer_resource_rule(http_method: str,
                             url_pattern: str,
                             access_type: str,
                             operation_name: str,
                             action_code: Optional[str] = None,
                             context_types: Optional[Set[ContextType]] = None,):
    """ Добавление описания ресурсного правила """

    def decorator(view_method):

        if not action_code:
            method_name = str(view_method.__name__).lower()
            lower_http_method = http_method.lower()

            code = method_name if method_name == lower_http_method else f'{lower_http_method}_{method_name}'
        else:
            code = action_code

        AuthorizerSchemaBuilder().add_resource_rule(http_method.upper(), url_pattern,
                                                    code, access_type, operation_name,
                                                    view_method.__qualname__,
                                                    context_types=context_types, )
        return view_method

    return decorator
