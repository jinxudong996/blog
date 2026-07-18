from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, model_validator


class ClaimKind(str, Enum):
    NARRATIVE_FACT = "narrative_fact"
    CHARACTER_STATEMENT = "character_statement"
    INFERENCE = "inference"


class ReviewStatus(str, Enum):
    AUTO_ACCEPTED = "auto_accepted"
    NEEDS_REVIEW = "needs_review"
    REJECTED = "rejected"


class Evidence(BaseModel):
    quote: str = Field(description="Exact, contiguous quote copied from source text")
    start: int | None = None
    end: int | None = None


class Claim(BaseModel):
    id: str
    subject: str
    predicate: str
    value: str | int | bool | None
    kind: ClaimKind
    evidence: list[Evidence] = Field(default_factory=list)
    speaker: str | None = None
    confidence: float = Field(default=1.0, ge=0, le=1)
    review_status: ReviewStatus = ReviewStatus.NEEDS_REVIEW
    validation_errors: list[str] = Field(default_factory=list)
    conflicts_with: list[str] = Field(default_factory=list)


class Character(BaseModel):
    name: str
    aliases: list[str] = Field(default_factory=list)
    identity: str | None = None
    goal: str | None = None
    traits: list[str] = Field(default_factory=list)
    source_claim_ids: list[str] = Field(
        default_factory=list,
        description="Claims supporting this complete character record",
    )


class Relationship(BaseModel):
    source: str
    target: str
    relation_type: str | None = None
    description: str | None = None
    source_claim_ids: list[str] = Field(default_factory=list)


class StoryEvent(BaseModel):
    sequence: int
    description: str
    participants: list[str] = Field(default_factory=list)
    cause: str | None = None
    result: str | None = None
    source_claim_ids: list[str] = Field(default_factory=list)


class Conflict(BaseModel):
    subject: str
    predicate: str
    claim_ids: list[str]
    values: list[str]
    status: str = "unresolved"


class ExtractionDraft(BaseModel):
    worldview: str | None = None
    characters: list[Character] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)
    events: list[StoryEvent] = Field(default_factory=list)
    unresolved_conflicts: list[str] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)


class StoryBible(BaseModel):
    worldview: str | None = None
    characters: list[Character] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)
    events: list[StoryEvent] = Field(default_factory=list)
    unresolved_conflicts: list[str] = Field(default_factory=list)


class ExtractionReport(BaseModel):
    story_bible: StoryBible
    candidate_bible: StoryBible
    claims: list[Claim]
    conflicts: list[Conflict] = Field(default_factory=list)
    source_sha256: str
    prompt_version: str
    publication_warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def accepted_claims_have_evidence(self):
        for claim in self.claims:
            if claim.review_status == ReviewStatus.AUTO_ACCEPTED and not claim.evidence:
                raise ValueError(f"Accepted claim {claim.id} has no evidence")
        return self
