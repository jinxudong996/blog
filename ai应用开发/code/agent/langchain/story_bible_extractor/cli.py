from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from .pipeline import extract_story


def create_model() -> ChatOpenAI:
    env_path = Path(__file__).resolve().parents[2] / ".ENV"
    load_dotenv(env_path)
    required = ["LLM_MODEL_ID", "LLM_API_KEY", "LLM_BASE_URL"]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise ValueError("Missing environment variables: " + ", ".join(missing))
    return ChatOpenAI(
        model=os.environ["LLM_MODEL_ID"],
        api_key=os.environ["LLM_API_KEY"],
        base_url=os.environ["LLM_BASE_URL"],
        temperature=0,
        timeout=int(os.getenv("LLM_TIMEOUT", "90")),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract an evidence-backed StoryBible")
    parser.add_argument("input", type=Path, help="UTF-8 story .txt file")
    parser.add_argument("--output", type=Path, default=Path("story_bible.json"))
    parser.add_argument("--report", type=Path, default=Path("extraction_report.json"))
    args = parser.parse_args()

    if not args.input.is_file():
        parser.error(
            f"input file does not exist: {args.input.resolve()}\n"
            "Paths are resolved relative to the current working directory."
        )

    story = args.input.read_text(encoding="utf-8")
    report = extract_story(story, create_model())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        report.story_bible.model_dump_json(indent=2), encoding="utf-8"
    )
    args.report.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    print(f"StoryBible: {args.output.resolve()}")
    print(f"Audit report: {args.report.resolve()}")
    print(f"Claims: {len(report.claims)}, conflicts: {len(report.conflicts)}")


if __name__ == "__main__":
    main()
