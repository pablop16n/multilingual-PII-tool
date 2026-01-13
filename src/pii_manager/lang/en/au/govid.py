"""
Australian Government-issued IDs:
  - TFN (Tax File Number)
"""

import re

from typing import Iterable

from stdnum.au import tfn

from pii_manager import PiiEnum, PiiEntity
from pii_manager.helper import BasePiiTask

# regex for TFN
_TFN_PATTERN = r"\b\d{8,9}\b"


class AustralianTFN(BasePiiTask):
    """
    Australian Government-issued TFN numbers, recognize & validate
    """

    pii_name = "Australian TFN"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Compile the regex
        self.tfn_pattern = re.compile(_TFN_PATTERN, flags=re.X)


    def find(self, doc: str) -> Iterable[PiiEntity]:
        # TFN
        for item in self.tfn_pattern.finditer(doc):
            item_value = item.group()
            if tfn.is_valid(item_value):
                yield PiiEntity(
                    PiiEnum.GOV_ID,
                    item.start(),
                    item_value,
                    country=self.country,
                    name=" Australian TFN",
                )

# Task descriptor
PII_TASKS = [(PiiEnum.GOV_ID, AustralianTFN)]