from typing import Optional


def safe_int(input: Optional[str]) -> int:
    if input is None:
        raise Exception("String is None")

    return int(input)
