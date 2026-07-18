from __future__ import annotations

import hashlib

from langchain_core.language_models.chat_models import BaseChatModel

from .models import ExtractionDraft, ExtractionReport, ReviewStatus, StoryBible
from .prompt import EXTRACTION_PROMPT, PROMPT_VERSION
from .validators import detect_conflicts, validate_claims


def build_chain(model: BaseChatModel):
    # OpenAI-compatible providers such as DeepSeek may reject JSON Schema
    # response_format, while supporting equivalent tool/function calling.
    structured_model = model.with_structured_output(
        ExtractionDraft,
        method="function_calling",
    )
    return EXTRACTION_PROMPT | structured_model


def extract_story(story: str, model: BaseChatModel) -> ExtractionReport:
    if not story.strip():
        raise ValueError("Story text cannot be empty")

    draft = build_chain(model).invoke({"story": story})
    if not isinstance(draft, ExtractionDraft):
        draft = ExtractionDraft.model_validate(draft)

    claims = validate_claims(draft.claims, story)
    conflicts = detect_conflicts(claims)
    candidate_bible = StoryBible(
        worldview=draft.worldview,
        characters=draft.characters,
        relationships=draft.relationships,
        events=draft.events,
        unresolved_conflicts=draft.unresolved_conflicts,
    )
    accepted_ids = {
        claim.id
        for claim in claims
        if claim.review_status == ReviewStatus.AUTO_ACCEPTED
    }
    warnings: list[str] = []

    def publish(items, label: str):
        published = []
        for item in items:
            ids = set(item.source_claim_ids)
            if ids and ids <= accepted_ids:
                published.append(item)
            else:
                warnings.append(
                    f"{label} not published because its source claims are missing or unaccepted: "
                    f"{sorted(ids)}"
                )
        return published

    bible = StoryBible(
        # Scalar summaries remain candidates until a later field-level review exists.
        worldview=None,
        characters=publish(draft.characters, "character"),
        relationships=publish(draft.relationships, "relationship"),
        events=publish(draft.events, "event"),
        unresolved_conflicts=[
            f"{item.subject}.{item.predicate}: {', '.join(item.values)}"
            for item in conflicts
        ],
    )
    return ExtractionReport(
        story_bible=bible,
        candidate_bible=candidate_bible,
        claims=claims,
        conflicts=conflicts,
        source_sha256=hashlib.sha256(story.encode("utf-8")).hexdigest(),
        prompt_version=PROMPT_VERSION,
        publication_warnings=warnings,
    )
