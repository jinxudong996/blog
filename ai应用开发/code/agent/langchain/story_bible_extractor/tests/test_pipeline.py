import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_core.runnables import RunnableLambda

from story_bible_extractor.models import ExtractionDraft
from story_bible_extractor.pipeline import extract_story


class FakeStructuredModel:
    def __init__(self, draft):
        self.draft = draft

    def with_structured_output(self, _schema, **_kwargs):
        return RunnableLambda(lambda _messages: self.draft)


class PipelineTests(unittest.TestCase):
    def test_only_evidence_backed_narrative_objects_are_published(self):
        draft = ExtractionDraft.model_validate(
            {
                "characters": [
                    {"name": "林晚", "source_claim_ids": ["claim-001"]},
                    {"name": "陈默", "source_claim_ids": ["claim-002"]},
                ],
                "claims": [
                    {
                        "id": "claim-001",
                        "subject": "林晚",
                        "predicate": "出现",
                        "value": True,
                        "kind": "narrative_fact",
                        "evidence": [{"quote": "林晚走进房间"}],
                    },
                    {
                        "id": "claim-002",
                        "subject": "陈默",
                        "predicate": "是凶手",
                        "value": True,
                        "kind": "character_statement",
                        "speaker": "林晚",
                        "evidence": [{"quote": "林晚说陈默是凶手"}],
                    },
                ],
            }
        )
        story = "林晚走进房间。林晚说陈默是凶手。"
        report = extract_story(story, FakeStructuredModel(draft))

        self.assertEqual([item.name for item in report.story_bible.characters], ["林晚"])
        self.assertEqual(len(report.candidate_bible.characters), 2)
        self.assertEqual(len(report.publication_warnings), 1)


if __name__ == "__main__":
    unittest.main()
