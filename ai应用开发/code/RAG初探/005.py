import os
from pathlib import Path

from unstructured.partition.text import partition_text


BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "企业知识库建设方案.txt"


def load_elements_by_title():
    """使用 Unstructured 的 by_title 策略读取并分块文档。"""

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"找不到文本文件: {DATA_FILE}")

    # strategy="hi_res"/"fast" 这里用默认文本分割即可，重点是 by_title
    elements = partition_text(
        filename=str(DATA_FILE),
        # by_title: 按标题组织块结构
        strategy="fast",
        by_title=True,
    )
    return elements


def print_chunks(elements):
    """打印按标题分块后的块信息，方便肉眼观察效果。"""

    print("=" * 80)
    print(f"使用 Unstructured by_title 对 {DATA_FILE.name} 的分块结果：")
    print("-" * 80)

    for i, el in enumerate(elements, start=1):
        # Unstructured 的元素通常有 .text 属性，有些还有 .metadata / .category
        text = getattr(el, "text", "").strip()
        category = getattr(el, "category", None)
        metadata = getattr(el, "metadata", None)

        # 只展示前 120 个字符，避免太长
        preview = (text[:120] + "...") if len(text) > 120 else text

        print(f"[块 {i}] 类型: {category}")
        if metadata is not None:
            # 有的元素会在 metadata 中带有标题信息（比如 parent_id / section）
            title = getattr(metadata, "text_as_html", None) or getattr(
                metadata, "filename", None
            )
        else:
            title = None

        # 这里 title 可能比较杂，主要看 category 和 preview
        if title:
            print(f"  可能相关标题/元信息: {title}")

        print(f"  内容预览: {preview}")
        print()


if __name__ == "__main__":
    elements = load_elements_by_title()
    print_chunks(elements)
