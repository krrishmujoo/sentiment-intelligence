from src.intelligence.planner_schema import (
    AnalysisPlan,
    PlannerOperation,
)
from src.intelligence.schemas import (
    InsightPacket,
)


def execute_operation(
    operation: PlannerOperation,
    packet: InsightPacket,
) -> dict:
    """
    Execute one validated planner operation
    against a privacy-safe InsightPacket.

    The executor never receives raw review data.
    """

    if operation.operation == "summarize_sentiment":

        return {
            "operation": operation.operation,
            "result": packet.dataset.model_dump(),
        }


    if operation.operation == "rank_priority_issues":

        limit = (
            operation.limit
            if operation.limit is not None
            else 5
        )

        return {
            "operation": operation.operation,
            "result": [
                item.model_dump()
                for item
                in packet.priority_issues[:limit]
            ],
        }


    if operation.operation == "summarize_themes":

        limit = (
            operation.limit
            if operation.limit is not None
            else 10
        )

        return {
            "operation": operation.operation,
            "result": [
                item.model_dump()
                for item
                in packet.themes[:limit]
            ],
        }


    if operation.operation == "filter_negative_themes":

        limit = (
            operation.limit
            if operation.limit is not None
            else 5
        )

        ranked = sorted(
            packet.themes,
            key=lambda item: (
                -item.negative_rate,
                -item.total_mentions,
                item.theme,
            ),
        )

        return {
            "operation": operation.operation,
            "result": [
                item.model_dump()
                for item
                in ranked[:limit]
            ],
        }


    if operation.operation == "filter_positive_themes":

        limit = (
            operation.limit
            if operation.limit is not None
            else 5
        )

        ranked = sorted(
            packet.themes,
            key=lambda item: (
                -item.positive_rate,
                -item.total_mentions,
                item.theme,
            ),
        )

        return {
            "operation": operation.operation,
            "result": [
                item.model_dump()
                for item
                in ranked[:limit]
            ],
        }


    if operation.operation == "summarize_uncertainty":

        return {
            "operation": operation.operation,
            "result": {
                "uncertainty_rate": (
                    packet.dataset.uncertainty_rate
                ),
                "average_confidence": (
                    packet.dataset.average_confidence
                ),
            },
        }


    raise ValueError(
        f"Unsupported operation: "
        f"{operation.operation}"
    )


def execute_plan(
    plan: AnalysisPlan,
    packet: InsightPacket,
) -> dict:
    """
    Execute a complete validated analysis plan
    using only privacy-safe aggregate data.
    """

    if not isinstance(
        plan,
        AnalysisPlan,
    ):
        raise TypeError(
            "plan must be an AnalysisPlan"
        )

    if not isinstance(
        packet,
        InsightPacket,
    ):
        raise TypeError(
            "packet must be an InsightPacket"
        )

    results = [
        execute_operation(
            operation,
            packet,
        )
        for operation in plan.operations
    ]

    return {
        "intent": plan.intent,
        "results": results,
    }