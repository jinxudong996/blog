"""Reusable prompt library for LangChain demos."""

from prompt_library.article_prompts import (
    CATEGORY_PROMPT_VERSION,
    KEYWORDS_PROMPT_VERSION,
    SENTIMENT_PROMPT_VERSION,
    SUMMARY_PROMPT_VERSION,
    category_prompt,
    keywords_prompt,
    sentiment_prompt,
    summary_prompt,
)
from prompt_library.output_prompts import FINAL_ANSWER_PROMPT_VERSION, final_answer_prompt
from prompt_library.router_prompts import TASK_IDENTIFY_PROMPT_VERSION, task_identify_prompt


PROMPT_VERSIONS = {
    "summary": SUMMARY_PROMPT_VERSION,
    "keywords": KEYWORDS_PROMPT_VERSION,
    "category": CATEGORY_PROMPT_VERSION,
    "sentiment": SENTIMENT_PROMPT_VERSION,
    "task_identify": TASK_IDENTIFY_PROMPT_VERSION,
    "final_answer": FINAL_ANSWER_PROMPT_VERSION,
}


__all__ = [
    "CATEGORY_PROMPT_VERSION",
    "FINAL_ANSWER_PROMPT_VERSION",
    "KEYWORDS_PROMPT_VERSION",
    "PROMPT_VERSIONS",
    "SENTIMENT_PROMPT_VERSION",
    "SUMMARY_PROMPT_VERSION",
    "TASK_IDENTIFY_PROMPT_VERSION",
    "category_prompt",
    "final_answer_prompt",
    "keywords_prompt",
    "sentiment_prompt",
    "summary_prompt",
    "task_identify_prompt",
]
