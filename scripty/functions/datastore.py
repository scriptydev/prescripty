# Copyright © tandemdude 2020-present
#
# NOTE: This is a adapted copy of the DataStore implmentation from the
# Lightbulb command handler. It is ported over in order to add the feature
# in this program which uses the Tanjun framework.
#
# Repository source from https://github.com/tandemdude/hikari-lightbulb.
from __future__ import annotations

__all__ = ["DataStore"]

from typing import Any


class DataStore(dict[str, Any]):
    """
    Data storage class allowing setting, retrieval and unsetting of custom
    attributes. This class subclasses dict so the data can be accessed the same
    as you would a dictionary as well as using dot notation.
    """

    def __repr__(self) -> str:
        return "DataStore(" + ", ".join(f"{k}={v!r}" for k, v in self.items()) + ")"

    def __getattr__(self, item: str) -> Any:
        return self.get(item)

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value

    def __delattr__(self, item: str) -> None:
        self.pop(item, None)
