from pathlib import Path


def load_prompt(prompt_name: str) -> str:
    """
    Load a prompt from the prompts directory.

    Args:
        prompt_name (str): The name of the prompt file to load.

    Returns:
        str: The content of the prompt file.
    """
    current_dir = Path(__file__).parent
    prompt_path = current_dir / f"{prompt_name}.md"
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt = file.read().strip()
    return prompt
