import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from story_bible_extractor.models import Claim, ClaimKind, ReviewStatus
from story_bible_extractor.validators import detect_conflicts, validate_claims


class ValidatorTests(unittest.TestCase):
    def test_exact_evidence_is_accepted(self):
        claim = Claim(
            id="claim-001",
            subject="林晚",
            predicate="动作",
            value="进入房间",
            kind=ClaimKind.NARRATIVE_FACT,
            evidence=[{"quote": "林晚进入房间"}],
        )
        result = validate_claims([claim], "林晚进入房间")
        self.assertEqual(result[0].review_status, ReviewStatus.AUTO_ACCEPTED)
        self.assertEqual(result[0].evidence[0].start, 0)

    def test_fabricated_evidence_is_rejected(self):
        claim = Claim(
            id="claim-001",
            subject="林晚",
            predicate="职业",
            value="医生",
            kind=ClaimKind.NARRATIVE_FACT,
            evidence=[{"quote": "林晚是一名医生"}],
        )
        result = validate_claims([claim], "林晚穿着白大褂进入房间")
        self.assertEqual(result[0].review_status, ReviewStatus.REJECTED)

    def test_conflicting_values_need_review(self):
        claims = [
            Claim(id="claim-001", subject="陈默", predicate="年龄", value=25,
                  kind=ClaimKind.NARRATIVE_FACT, evidence=[{"quote": "陈默25岁"}]),
            Claim(id="claim-002", subject="陈默", predicate="年龄", value=28,
                  kind=ClaimKind.NARRATIVE_FACT, evidence=[{"quote": "陈默28岁"}]),
        ]
        validate_claims(claims, "陈默25岁。后来，陈默28岁。")
        conflicts = detect_conflicts(claims)
        self.assertEqual(len(conflicts), 1)
        self.assertTrue(all(c.review_status == ReviewStatus.NEEDS_REVIEW for c in claims))


if __name__ == "__main__":
    unittest.main()
