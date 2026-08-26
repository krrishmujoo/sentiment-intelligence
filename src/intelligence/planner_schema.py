from typing import Literal

from pydantic import BaseModel


PlannerOperationName = Literal[
    "summarize_sentiment",
    "rank_priority_issues",
    "summarize_themes",
    "filter_negative_themes",
    "filter_positive_themes",
    "summarize_uncertainty",
]


class PlannerOperation(BaseModel):
    """
    One allowed analytics operation requested
    by the future LLM planner.

    The planner is only allowed to choose from
    a fixed whitelist of operation names.
    """

    operation: PlannerOperationName

    limit: int | None = None


class AnalysisPlan(BaseModel):
    """
    Validated plan produced by the future
    planner layer.

    The LLM will not execute code directly.
    It will only propose one of these plans.
    """

    intent: str

    operations: list[PlannerOperation]