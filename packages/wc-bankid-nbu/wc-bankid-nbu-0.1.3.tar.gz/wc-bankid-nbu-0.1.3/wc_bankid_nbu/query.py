from typing import Any, Sequence, TypeVar
from copy import deepcopy


__all__ = 'QueryBuilder', 'FieldsDataQuery', 'PersonalPhysicalDataQuery'


T = TypeVar('T')


class QueryBuilder:
    query: dict

    def __init__(self, query: dict = {}):
        self.query = query

    def clone(self, query: dict):
        return deepcopy(query)

    def nest(self) -> 'QueryBuilder':
        return self.__class__(query=self.clone(self.query))

    def to_foreign(self) -> Any:
        raise NotImplementedError(
            'Implement final query transformation in `to_foreign` method.'
        )


class FieldsDataQuery(QueryBuilder):
    def _set(self: T, *path: Sequence[str], fields: Sequence[str]) -> T:
        s = self.nest()
        q: dict = s.query
        last = path[-1]

        for key in path:
            if key not in q:
                if key is last:
                    q[key] = q.get(key) or set()
                else:
                    q[key] = q.get(key) or {}

            q = q[key]

        q: set = q
        q.update(fields)

        return s


class PersonalPhysicalDataQuery(FieldsDataQuery):
    def fields(self: T, *fields: Sequence[str]) -> T:
        return self._set('fields', fields=fields)

    def address(self: T, type: str, *fields: Sequence[str]) -> T:
        return self._set('addresses', type, 'fields', fields=fields)

    def document(self: T, type: str, *fields: Sequence[str]) -> T:
        return self._set('documents', type, 'fields', fields=fields)

    def scan(self: T, type: str, *fields: Sequence[str]) -> T:
        return self._set('scans', type, 'fields', fields=fields)

    def _collect_typed_fields(self, query_part: dict) -> Sequence[dict]:
        return [
            {'type': type, 'fields': list(data['fields'])}
            for type, data in query_part.items()
        ]

    def to_foreign(self) -> dict:
        result = {
            'type': 'physical',
            'fields': list(self.query.get('fields', [])),
            'addresses': self._collect_typed_fields(self.query.get('addresses', {})),
            'documents': self._collect_typed_fields(self.query.get('documents', {})),
            'scans': self._collect_typed_fields(self.query.get('scans', {})),
        }

        for key, item in list(result.items()):
            if not item or len(item) == 0:
                result.pop(key)

        return result
