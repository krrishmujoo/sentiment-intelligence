from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from src.intelligence.claude_insight import (
    generate_business_insights,
)


class FakeMessages:
    def __init__(self, response_text):
        self.response_text = response_text
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)

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


def sample_execution_result():
    return {
        "intent": "identify_top_customer_complaints",
        "results": [
            {
                "operation": "rank_priority_issues",
                "result": [
                    {
                        "theme": "performance",
                        "total_mentions": 10,
                        "negative_rate": 0.7,
                        "frequency_share": 0.4,
                        "priority_score": 0.28,
                    }
                ],
            }
        ],
    }


def test_valid_business_insight_response():
    fake_response = """
    {
      "summary": "Performance is the leading issue in this batch.",
      "observations": [
        {
          "title": "Performance is a priority issue",
          "description": "Performance has the highest supplied priority score.",
          "evidence": [
            "10 mentions",
            "70% negative rate",
            "Priority score: 0.28"
          ]
        }
      ],
      "recommendations": [
        {
          "title": "Investigate performance bottlenecks",
          "action": "Review the most common slow workflows and recent regressions.",
          "rationale": "Performance combines meaningful frequency with a high negative rate.",
          "priority": "high"
        }
      ]
    }
    """

    client = FakeClaudeClient(
        fake_response
    )

    result = generate_business_insights(
        "What should the product team focus on?",
        sample_execution_result(),
        client=client,
    )

    assert (
        result.summary
        == "Performance is the leading issue in this batch."
    )

    assert len(
        result.observations
    ) == 1

    assert (
        result.observations[0].title
        == "Performance is a priority issue"
    )

    assert len(
        result.recommendations
    ) == 1

    assert (
        result.recommendations[0].priority
        == "high"
    )


def test_markdown_json_fences_are_cleaned():
    fake_response = """
    ```json
    {
      "summary": "Performance needs attention.",
      "observations": [],
      "recommendations": []
    }
    ```
    """

    client = FakeClaudeClient(
        fake_response
    )

    result = generate_business_insights(
        "What matters most?",
        sample_execution_result(),
        client=client,
    )

    assert (
        result.summary
        == "Performance needs attention."
    )


def test_invalid_json_is_rejected():
    client = FakeClaudeClient(
        "not valid json"
    )

    with pytest.raises(
        RuntimeError,
        match="invalid JSON",
    ):
        generate_business_insights(
            "What matters most?",
            sample_execution_result(),
            client=client,
        )


def test_empty_response_is_rejected():
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
        generate_business_insights(
            "What matters most?",
            sample_execution_result(),
            client=EmptyClient(),
        )


def test_invalid_priority_is_rejected():
    fake_response = """
    {
      "summary": "Performance needs attention.",
      "observations": [],
      "recommendations": [
        {
          "title": "Fix performance",
          "action": "Investigate slow workflows.",
          "rationale": "Performance has negative sentiment.",
          "priority": "urgent"
        }
      ]
    }
    """

    client = FakeClaudeClient(
        fake_response
    )

    with pytest.raises(
        ValidationError
    ):
        generate_business_insights(
            "What matters most?",
            sample_execution_result(),
            client=client,
        )


def test_payload_contains_only_safe_analytics():
    captured_kwargs = {}

    class RecordingMessages:
        def create(self, **kwargs):
            captured_kwargs.update(
                kwargs
            )

            return SimpleNamespace(
                content=[
                    SimpleNamespace(
                        text="""
                        {
                          "summary": "Performance needs attention.",
                          "observations": [],
                          "recommendations": []
                        }
                        """
                    )
                ]
            )

    class RecordingClient:
        messages = RecordingMessages()

    execution_result = (
        sample_execution_result()
    )

    generate_business_insights(
        "What should we fix first?",
        execution_result,
        client=RecordingClient(),
    )

    serialized_request = str(
        captured_kwargs
    ).lower()

    assert (
        "what should we fix first?"
        in serialized_request
    )

    assert "performance" in serialized_request
    assert "priority_score" in serialized_request

    # Raw review text must not appear.
    assert (
        "the app crashes every time"
        not in serialized_request
    )

    assert (
        "customer@example.com"
        not in serialized_request
    )


def test_invalid_input_types_are_rejected():
    client = FakeClaudeClient(
        """
        {
          "summary": "Safe response.",
          "observations": [],
          "recommendations": []
        }
        """
    )

    with pytest.raises(TypeError):
        generate_business_insights(
            123,
            sample_execution_result(),
            client=client,
        )

    with pytest.raises(ValueError):
        generate_business_insights(
            "   ",
            sample_execution_result(),
            client=client,
        )

    with pytest.raises(TypeError):
        generate_business_insights(
            "What matters?",
            [],
            client=client,
        )