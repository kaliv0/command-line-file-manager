import os
from typing import Unpack


def should_skip_hidden(show_hidden: bool, *paths: Unpack[str]) -> bool:
    return not show_hidden and any(os.path.basename(entry).startswith(".") for entry in paths)
