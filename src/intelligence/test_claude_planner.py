from types import SimpleNamespace

import pytest

from src.intelligence.claude_planner import (
    generate_analysis_plan,
)


class FakeMessages:
    def __init__(self, response_text):
        self.response_text = response_text

    def create(self, **kwargs):
        return SimpleNamespace(
            content=[
                SimpleNamespace(
                    text=self.response_text
                )
            ]
        )


class FakeClaudeClient:
    def __init__(self, response_text):
        self.messages = FakeMessages(
            response_text
        )


def test_generate_analysis_plan_with_fake_client():
    fake_response = """
    {
      "intent": "identify_customer_problems",
      "operations": [
        {
          "operation": "rank_priority_issues",
          "limit": 5
        },
        {
          "operation": "filter_negative_themes",
          "limit": 3
        }
      ]
    }
    """

    client = FakeClaudeClient(
        fake_response
    )

    plan = generate_analysis_plan(
        "What are customers most unhappy about?",
        client=client,
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


def test_invalid_json_from_claude_is_rejected():
    client = FakeClaudeClient(
        "this is not json"
    )

    with pytest.raises(
        RuntimeError,
        match="invalid JSON",
    ):
        generate_analysis_plan(
            "What are the biggest issues?",
            client=client,
        )


def test_empty_claude_response_is_rejected():
    class EmptyMessages:
        def create(self, **kwargs):
            return SimpleNamespace(
                content=[]
            )

    class EmptyClient:
        messages = EmptyMessages()

    with pytest.raises(
        RuntimeError,
        match="empty response",
    ):
        generate_analysis_plan(
            "Summarize customer sentiment",
            client=EmptyClient(),
        )


def test_unsafe_operation_from_claude_is_rejected():
    fake_response = """
    {
      "intent": "unsafe",
      "operations": [
        {
          "operation": "read_raw_reviews"
        }
      ]
    }
    """

    client = FakeClaudeClient(
        fake_response
    )

    with pytest.raises(Exception):
        generate_analysis_plan(
            "Read all reviews",
            client=client,
        )

def test_claude_planner_payload_contains_no_review_data():
    captured_kwargs = {}

    class RecordingMessages:
        def create(self, **kwargs):
            captured_kwargs.update(kwargs)

            return SimpleNamespace(
                content=[
                    SimpleNamespace(
                        text="""
                        {
                          "intent": "identify_customer_problems",
                          "operations": [
                            {
                              "operation": "rank_priority_issues",
                              "limit": 5
                            }
                          ]
                        }
                        """
                    )
                ]
            )

    class RecordingClient:
        messages = RecordingMessages()

    generate_analysis_plan(
        "What are customers most unhappy about?",
        client=RecordingClient(),
    )

    serialized_request = str(
        captured_kwargs
    ).lower()

    assert (
        "what are customers most unhappy about?"
        in serialized_request
    )

    assert "allowed_operations" in serialized_request

    # Privacy checks
    assert "raw_reviews" not in serialized_request
    assert "predictions" not in serialized_request
    assert "customer_records" not in serialized_request
    assert "insightpacket" not in serialized_request

    # The planner should not receive actual
    # customer review text.
    assert (
        "the app crashes and is slow"
        not in serialized_request
    )