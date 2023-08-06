from typing import Any, List, Optional, Sequence, TypeVar
from django.db import models
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from wcd_geo_db.const import DivisionLevel
from wcd_geo_db.modules.code_seeker.query import CodeSeekerQuerySet
from pxd_tree.hierarchy import TreeQuerySet

from ..dtos import DivisionDTO, GeometryDTO
from .base import QuerySet
from .geometry import WithGeometryQuerySet
from .search import SearchQueryParam, SearchQuerySet


__all__ = 'DivisionsQuerySet',

QT = TypeVar('QT', bound='DivisionsQuerySet')
VALUES_NAMES = (
    'id', 'name', 'level', 'types', 'codes', 'parent_id', 'path',
    'geometry__location', 'geometry__polygon',
)


def as_dto(values: dict) -> DivisionDTO:
    return DivisionDTO(
        id=values['id'],
        name=values['name'],
        level=DivisionLevel(values['level']),
        types=values['types'],
        codes=values['codes'],
        parent_id=values['parent_id'],
        path=list(values['path']),
        geometry=GeometryDTO(
            location=values['geometry__location'],
            polygon=values['geometry__polygon'],
        )
    )


class DivisionsQuerySet(
    WithGeometryQuerySet,
    CodeSeekerQuerySet,
    TreeQuerySet,
    SearchQuerySet,
    QuerySet
):
    SEARCH_QUERY_MIN_LENGTH: int = 2
    SEARCH_QUERY_RANK_WEIGHTS: Sequence[float] = [0.2, 0.4, 0.8, 1]

    def search(self: QT, query: SearchQueryParam) -> QT:
        q = query.get('query')

        if not q or len(q) < self.SEARCH_QUERY_MIN_LENGTH:
            return self

        vector = (
            SearchVector('name', weight='A')
            +
            SearchVector('synonyms', weight='B')
        )
        sql_query = SearchQuery(q, search_type='websearch')
        rank = SearchRank(
            vector, sql_query, weights=self.SEARCH_QUERY_RANK_WEIGHTS
        )

        return (
            self
            .annotate(search=vector, rank=rank)
            .filter(search=sql_query)
            .order_by('-rank')
        )

    def as_dtos(self) -> List[DivisionDTO]:
        return [as_dto(values) for values in self.values(*VALUES_NAMES)]

    def general_filter(
        self: QT,
        parent_ids: Optional[Sequence[int]] = None,
        levels: Optional[Sequence[DivisionLevel]] = None,
        types: Optional[Sequence[str]] = None,
        **kw
    ) -> QT:
        q = (
            super().general_filter(**kw)
            .optional_in('parent_id', parent_ids)
            .optional_in('level', levels)
            .optional_overlap('types', types)
        )

        return q
