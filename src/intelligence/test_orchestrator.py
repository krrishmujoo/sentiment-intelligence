from types import SimpleNamespace

from src.intelligence.orchestrator import (
    analyze_business_question,
)


class SequencedMessages:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)

        response_text = self.responses.pop(0)

        return SimpleNamespace(
            content=[
                SimpleNamespace(
                    text=response_text
                )
            ]
        )


class FakeClaudeClient:
    def __init__(self, responses):
        self.messages = SequencedMessages(
            responses
        )


def sample_predictions():
    return [
        {
            "review": (
                "The app crashes and is very slow."
            ),
            "sentiment": "negative",
            "confidence": 0.91,
            "prediction_margin": 0.70,
            "is_uncertain": False,
        },
        {
            "review": (
                "The app is useful but sometimes slow."
            ),
            "sentiment": "neutral",
            "confidence": 0.52,
            "prediction_margin": 0.08,
            "is_uncertain": True,
        },
        {
            "review": (
                "The interface is easy to use."
            ),
            "sentiment": "positive",
            "confidence": 0.90,
            "prediction_margin": 0.72,
            "is_uncertain": False,
        },
    ]


def test_full_orchestrator_pipeline():
    planner_response = """
    {
      "intent": "identify_customer_problems",
      "operations": [
        {
          "operation": "rank_priority_issues",
          "limit": 5
        },
        {
          "operation": "filter_negative_themes",
          "limit": 5
        }
      ]
    }
    """

    insight_response = """
    {
      "summary": "Performance is the main issue in this sample.",
      "observations": [
        {
          "title": "Performance appears frequently",
          "description": "Performance is mentioned more often than other negative themes.",
          "evidence": [
            "performance appears in 2 theme mentions"
          ]
        }
      ],
      "recommendations": [
        {
          "title": "Investigate performance",
          "action": "Review performance-related workflows.",
          "rationale": "Performance combines meaningful frequency with negative sentiment.",
          "priority": "high"
        }
      ]
    }
    """

    client = FakeClaudeClient(
        [
            planner_response,
            insight_response,
        ]
    )

    result = analyze_business_question(
        "What should we fix first?",
        sample_predictions(),
        client=client,
    )

    assert (
        result["question"]
        == "What should we fix first?"
    )

    assert (
        result["plan"]["intent"]
        == "identify_customer_problems"
    )

    assert (
        len(
            result["plan"]["operations"]
        )
        == 2
    )

    assert "dataset" in result["analytics"]
    assert "themes" in result["analytics"]
    assert "priority_issues" in result["analytics"]

    assert (
        result["execution"]["intent"]
        == "identify_customer_problems"
    )

    assert (
        result["insights"]["summary"]
        == "Performance is the main issue in this sample."
    )

    assert (
        result["insights"][
            "recommendations"
        ][0]["priority"]
        == "high"
    )

    # Planner call + insight call
    assert len(
        client.messages.calls
    ) == 2


def test_raw_reviews_are_not_sent_to_claude():
    planner_response = """
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

    insight_response = """
    {
      "summary": "Performance needs attention.",
      "observations": [],
      "recommendations": []
    }
    """

    client = FakeClaudeClient(
        [
            planner_response,
            insight_response,
        ]
    )

    predictions = sample_predictions()

    analyze_business_question(
        "What should we fix first?",
        predictions,
        client=client,
    )

    all_requests = str(
        client.messages.calls
    ).lower()

    for prediction in predictions:
        assert (
            prediction["review"].lower()
            not in all_requests
        )