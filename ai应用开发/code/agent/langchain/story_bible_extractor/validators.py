from __future__ import annotations

from collections import defaultdict

from .models import Claim, ClaimKind, Conflict, ReviewStatus


def validate_claims(claims: list[Claim], source: str) -> list[Claim]:
    """Apply deterministic evidence and risk rules to model-produced claims."""
    seen_ids: set[str] = set()
    for claim in claims:
        errors: list[str] = []
        if claim.id in seen_ids:
            errors.append("duplicate claim id")
        seen_ids.add(claim.id)

        if not claim.evidence:
            errors.append("missing evidence")
        for evidence in claim.evidence:
            pos = source.find(evidence.quote)
            if pos < 0:
                errors.append(f"quote not found in source: {evidence.quote!r}")
            else:
                evidence.start = pos
                evidence.end = pos + len(evidence.quote)

        claim.validation_errors = errors
        if errors:
            claim.review_status = ReviewStatus.REJECTED
        elif claim.kind == ClaimKind.NARRATIVE_FACT:
            claim.review_status = ReviewStatus.AUTO_ACCEPTED
        else:
            claim.review_status = ReviewStatus.NEEDS_REVIEW
    return claims


def detect_conflicts(claims: list[Claim]) -> list[Conflict]:
    """Find exact subject/predicate groups with multiple scalar values."""
    groups: dict[tuple[str, str], list[Claim]] = defaultdict(list)
    for claim in claims:
        if claim.review_status != ReviewStatus.REJECTED and claim.value is not None:
            groups[(claim.subject.strip(), claim.predicate.strip())].append(claim)

    conflicts: list[Conflict] = []
    for (subject, predicate), group in groups.items():
        values = {str(item.value).strip() for item in group}
        if len(values) < 2:
            continue
        ids = [item.id for item in group]
        conflicts.append(
            Conflict(
                subject=subject,
                predicate=predicate,
                claim_ids=ids,
                values=sorted(values),
            )
        )
        for claim in group:
            claim.conflicts_with = [item for item in ids if item != claim.id]
            claim.review_status = ReviewStatus.NEEDS_REVIEW
    return conflicts
