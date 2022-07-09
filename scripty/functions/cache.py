from __future__ import annotations

__all__: tuple[str, ...] = ("LRUCachedDict",)

from collections import OrderedDict
from typing import Any


# https://gist.github.com/davesteele/44793cd0348f59f8fadd49d7799bd306
class LRUCachedDict(OrderedDict[Any, Any]):
    """Dict with a limited length, ejecting LRUs as needed."""

    def __init__(self, *args: Any, cache_len: int, **kwargs: Any):
        self.cache_len = cache_len

        super().__init__(*args, **kwargs)

    def __setitem__(self, key: Any, value: Any):
        """Set an item in the cache dict and move to end."""
        super().__setitem__(key, value)
        super().move_to_end(key)

        while len(self) > self.cache_len:
            old_key = next(iter(self))
            super().__delitem__(old_key)

    def __getitem__(self, key: Any):
        """Get an item from the cache dict and move to end."""
        val = super().__getitem__(key)
        super().move_to_end(key)

        return val
