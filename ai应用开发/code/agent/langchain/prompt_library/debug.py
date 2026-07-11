"""Prompt debugging helpers."""


def preview_prompt(prompt, input_data: dict) -> None:
    """Print the final prompt string and message list before model invocation."""
    prompt_value = prompt.invoke(input_data)

    print("=== Prompt String ===")
    print(prompt_value.to_string())

    print("\n=== Prompt Messages ===")
    for message in prompt_value.to_messages():
        print(f"[{message.type}] {message.content}")
