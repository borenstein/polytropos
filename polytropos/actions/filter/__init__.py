from polytropos.actions.filter._filter import Filter


def register_filter_subclasses() -> None:
    """Import all built-in subclasses so that they can be used in tasks"""
    from polytropos.actions.filter.firstlast import EarliestFilter, LatestFilter
    from polytropos.actions.filter.multivariate.has_all import HasAllSpecificValues
    from polytropos.actions.filter.multivariate.has_any import HasAnySpecificValues
    from polytropos.actions.filter.univariate.comparison import AtLeast, AtMost, GreaterThan, LessThan, NotEqualTo
    from polytropos.actions.filter.univariate.exists import Exists, DoesNotExist
    from polytropos.actions.filter.sequential_filter import SequentialFilter
    from polytropos.actions.filter.nested_filter import NestedFilter
    from polytropos.actions.filter.univariate.one_of import MatchesOneOf, ContainsOneOf
    from polytropos.actions.filter.logical_operators.and_operator import And
    from polytropos.actions.filter.logical_operators.or_operator import Or
    from polytropos.actions.filter.logical_operators.not_operator import Not
