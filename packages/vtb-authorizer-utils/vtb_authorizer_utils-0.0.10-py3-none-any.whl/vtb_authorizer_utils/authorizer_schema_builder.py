import enum
from typing import Optional, Set
from singleton3 import Singleton


class ContextType(enum.Enum):
    """ Типы контекста """
    ORGANIZATIONS = 'Organizations'  # Контекст организации
    FOLDERS = 'Folders'  # Контекст папки
    PROJECTS = 'Projects'  # Контекст проекта
    DEFAULT = 'Default'  # Без контекста


class AuthorizerSchemaBuilder(metaclass=Singleton):
    """ Построение схемы импорта сервиса в Authorizer """

    def __init__(self):
        self.data = {}
        # Временное хранилище данных функций
        self._tmp_views_data = {}

    def add_service(self, name: str,
                    title: str,
                    url: str,
                    description: Optional[str] = None) -> 'AuthorizerSchemaBuilder':
        """ Добавление информации о сервисе для импорта в Authorizer """
        service_name = name.lower()
        if service_name not in self.data:
            self.data[service_name] = {
                'title': title,
                'description': description,
                'url': url,
                'resource_types': {},
                'resource_rules': []
            }

        return self

    def add_resource_type(self, service: str,
                          name: str,
                          qualified_name: str,
                          title: Optional[str],
                          description: Optional[str]) -> 'AuthorizerSchemaBuilder':
        """ Добавление информации о ресурсном типе для импорта в Authorizer """
        service = service.lower()
        if service in self.data:
            name = name.lower()
            actions = set()
            for key in list(self._tmp_views_data.keys()):
                if str(key).startswith(qualified_name):
                    value = self._tmp_views_data.pop(key)
                    key_parts = str(key).split('-')
                    action_code = str(key_parts[1]).lower()
                    resource_action_code = f'{service}:{name}:{action_code}'
                    actions.add(action_code)

                    value['resource_action_code'] = resource_action_code

                    self.data[service]['resource_rules'].append(value)

            self.data[service]['resource_types'][name] = {
                'title': title,
                'description': description,
                'actions': ','.join(actions)
            }

        return self

    def add_resource_rule(self,
                          http_method: str,
                          url_pattern: str,
                          action_code: str,
                          access_type: str,
                          operation_name: str,
                          qualified_name: str,
                          context_types: Optional[Set[ContextType]] = None, ) -> 'AuthorizerSchemaBuilder':
        """ Добавление информации о ресурсном правиле для импорта в Authorizer """

        if context_types:
            for context_type in context_types:
                context_type = self._CONTEXT_TYPES_MAP[context_type]
                key = f'{qualified_name}-{action_code}-{context_type}'

                self._tmp_views_data[key] = {
                    'http_method': http_method,
                    'url_pattern': url_pattern.replace('{context_type}', context_type),
                    'access_type': access_type,
                    'operation_name': operation_name
                }
        else:
            key = f'{qualified_name}-{action_code}-default'

            self._tmp_views_data[key] = {
                'http_method': http_method,
                'url_pattern': url_pattern,
                'access_type': access_type,
                'operation_name': operation_name
            }

        return self

    _CONTEXT_TYPES_MAP = {
        ContextType.ORGANIZATIONS: 'organizations',
        ContextType.FOLDERS: 'folders',
        ContextType.PROJECTS: 'projects',
    }


def authorizer_service(name: str,
                       title: str,
                       url: str,
                       description: Optional[str] = None) -> 'AuthorizerSchemaBuilder':
    """ Добавление информации о сервисе для импорта в Authorizer """
    return AuthorizerSchemaBuilder().add_service(name,
                                                 title,
                                                 url,
                                                 description=description)
