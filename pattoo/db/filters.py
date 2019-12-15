#!/usr/bin/env python3
"""pattoo graphene_sqlalchemy_filter definitions."""

# PIP3 imports
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

# pattoo imports
from .models import PairXlate


class PairXlateFilter(FilterSet):
    """Filters for the PairXlate database table."""

    class Meta:
        """Filters for the PairXlate database table.

        model: SQLAlchemy table definition
        fields: Fields to filter on. Comprised of a dict keyed by table column
            name with values being a list of filter operators.

        A complete list of filter operators can be found here:
            https://pypi.org/project/graphene-sqlalchemy-filter/

        """

        model = PairXlate
        fields = {'idx_pair_xlate_group': ['eq']}


class PattooFilterableConnectionField(FilterableConnectionField):
    """A collection of filters to be used by GraphQL.

    filters: A dict keyed by SQLAlchemy table object with a corresponding
        instantiated filter for the table.

    """

    filters = {PairXlate: PairXlateFilter()}
