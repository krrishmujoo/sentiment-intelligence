import pytest
from pydantic import ValidationError

from src.intelligence.planner import (
    ALLOWED_OPERATIONS,
    build_planner_context,
    parse_planner_response,
)


def test_build_planner_context():
    context = build_planner_context(
        "What are customers most unhappy about?"
    )

    assert (
        context["user_question"]
        == "What are customers most unhappy about?"
    )

    assert (
        context["allowed_operations"]
        == ALLOWED_OPERATIONS
    )


def test_planner_context_contains_no_raw_data_fields():
    """
    Planner context should contain only the
    question and the allowed operation registry.
    """

    context = build_planner_context(
        "What are the biggest customer problems?"
    )

    assert set(
        context.keys()
    ) == {
        "user_question",
        "allowed_operations",
    }

    serialized = str(
        context
    ).lower()

    assert "reviews" not in serialized
    assert "predictions" not in serialized
    assert "customer_records" not in serialized


def test_empty_question_rejected():
    with pytest.raises(ValueError):
        build_planner_context(
            "   "
        )


def test_non_string_question_rejected():
    with pytest.raises(TypeError):
        build_planner_context(
            123
        )


def test_valid_planner_response_is_parsed():
    response = {
        "intent":
            "identify_customer_problems",

        "operations": [
            {
                "operation":
                    "rank_priority_issues",

                "limit": 5,
            },
            {
                "operation":
                    "filter_negative_themes",

                "limit": 3,
            },
        ],
    }

    plan = parse_planner_response(
        response
    )

    assert (
        plan.intent
        == "identify_customer_problems"
    )

    assert len(
        plan.operations
    ) == 2

    assert (
        plan.operations[0].operation
        == "rank_priority_issues"
    )

    assert (
        plan.operations[0].limit
        == 5
    )


def test_unsafe_operation_is_rejected():
    response = {
        "intent": "unsafe",

        "operations": [
            {
                "operation":
                    "read_raw_reviews",
            }
        ],
    }

    with pytest.raises(
        ValidationError
    ):
        parse_planner_response(
            response
        )


def test_non_dictionary_response_rejected():
    with pytest.raises(TypeError):
        parse_planner_response(
            "not a dictionary"
        )


def test_all_registered_operations_are_supported_by_schema():
    """
    Protect against accidentally adding an operation
    to the planner registry that the schema does not
    actually allow.
    """

    for operation_name in (
        ALLOWED_OPERATIONS
    ):
        response = {
            "intent": "test",

            "operations": [
                {
                    "operation":
                        operation_name
                }
            ],
        }

        plan = parse_planner_response(
            response
        )

        assert (
            plan.operations[0].operation
            == operation_name
        )