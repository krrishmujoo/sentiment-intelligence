from pydantic import BaseModel, Field


class InsightObservation(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
    )

    description: str = Field(
        min_length=1,
        max_length=300,
    )

    evidence: list[str] = Field(
        default_factory=list,
        max_length=3,
    )


class InsightRecommendation(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
    )

    action: str = Field(
        min_length=1,
        max_length=300,
    )

    rationale: str = Field(
        min_length=1,
        max_length=250,
    )

    priority: str = Field(
        pattern="^(high|medium|low)$"
    )


class BusinessInsightResponse(BaseModel):
    summary: str = Field(
        min_length=1,
        max_length=450,
    )

    observations: list[
        InsightObservation
    ] = Field(
        default_factory=list,
        max_length=3,
    )

    recommendations: list[
        InsightRecommendation
    ] = Field(
        default_factory=list,
        max_length=3,
    )