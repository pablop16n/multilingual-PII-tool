"""
Finnish Government-issued IDs:
  - HETU (Henkilötunnus)
"""

import re

from typing import Iterable

from stdnum.fi import hetu

from pii_manager import PiiEnum, PiiEntity
from pii_manager.helper import BasePiiTask

# regex for HETU
_HETU_PATTERN = r"\b[1-8]\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}\d\b"


class FinnishHETU(BasePiiTask):
    """
    Finnish Government-issued HETU numbers, recognize & validate
    """

    pii_name = "Finnish HETU"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Compile the regex
        self.hetu_pattern = re.compile(_HETU_PATTERN, flags=re.X)


    def find(self, doc: str) -> Iterable[PiiEntity]:
        # HETU
        for item in self.hetu_pattern.finditer(doc):
            item_value = item.group()
            if hetu.is_valid(item_value):
                yield PiiEntity(
                    PiiEnum.GOV_ID,
                    item.start(),
                    item_value,
                    country=self.country,
                    name=" Finnish HETU",
                )

# Task descriptor
PII_TASKS = [(PiiEnum.GOV_ID, FinnishHETU)]