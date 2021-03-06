import copy
from collections import Callable
from typing import Dict, List
from unittest.mock import MagicMock

import pytest
from polytropos.actions.filter.mem import InMemoryFilterIterator

from polytropos.actions.filter import Filter
from polytropos.actions.filter.univariate.exists import Exists
from polytropos.ontology.composite import Composite
from polytropos.ontology.context import Context

from polytropos.ontology.schema import Schema

@pytest.fixture()
def do_test(schema: Schema, composites: Dict) -> Callable:
    def _do_test(var_id: str, pass_condition: str, expected_keys: List[str]) -> None:
        context: Context = MagicMock(spec=Context)
        the_filter: Filter = Exists(context, schema, var_id, narrows=False, pass_condition=pass_condition)
        f_iter: Callable = InMemoryFilterIterator([the_filter])
        actual: List[Composite] = list(f_iter(composites.values()))
        expected: List[Composite] = []
        for key in expected_keys:
            expected.append(composites[key])
        assert actual == expected
    return _do_test

@pytest.mark.parametrize("pass_condition, expected_keys", [
    ("all", ["always"]),
    ("any", ["always", "middle", "earliest", "latest"]),
    ("earliest", ["always", "earliest"]),
    ("latest", ["always", "latest"]),
    ("never", ["immutable_only", "never"])
])
def test_temporal_cases(pass_condition: str, expected_keys: List[str], do_test: Callable) -> None:
    do_test("t_text", pass_condition, expected_keys)

@pytest.mark.parametrize("pass_condition", ["all", "any", "earliest", "latest", "never"])
def test_immutable_cases(pass_condition: str, do_test: Callable) -> None:
    expected_keys: List[str] = ["immutable_only", "never"]
    do_test("i_text", pass_condition, expected_keys)

@pytest.mark.parametrize("pass_condition", ["ALL", "All"])
def test_case_ignored(pass_condition: str, do_test: Callable) -> None:
    do_test("t_text", pass_condition, ["always"])

@pytest.mark.parametrize("pass_condition", ["all", "any", "earliest", "latest", "never"])
def test_no_effect_on_narrowing(pass_condition: str, schema: Schema, earliest_composite):
    context: Context = MagicMock(spec=Context)
    the_filter: Filter = Exists(context, schema, "t_text", filters=False, pass_condition=pass_condition)
    f_iter: Callable = InMemoryFilterIterator([the_filter])
    expected: List[Composite] = [copy.copy(earliest_composite)]
    del expected[0].content["period_2"]
    del expected[0].content["period_3"]
    actual: List[Composite] = list(f_iter([earliest_composite]))
    assert actual == expected
