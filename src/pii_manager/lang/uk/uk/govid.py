"""
Ukrainian Government-issued IDs:
  - РНОКПП (Reyestratsiyne Nomer Osoby Fizychnoyi Osoby)
"""

import re

from typing import Iterable


from pii_manager import PiiEnum, PiiEntity
from pii_manager.helper import BasePiiTask

# regex for RNO
_RNO_PATTERN = r"\b(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])\d{3}\d{2}\d{3}\d\b"


class UkrainianRNO(BasePiiTask):
    """
    Ukrainian Government-issued RNO numbers, recognize & validate
    """

    pii_name = "Ukrainian RNO"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Compile the regex
        self.rno_pattern = re.compile(_RNO_PATTERN, flags=re.X)

    def validate(self, rno: str) -> bool:
        rno = rno.strip()
        if not rno.isdigit() or len(rno) != 10:
            return False

        digits = [int(d) for d in rno]
        weights = [1,2,3,4,5,6,7,8,9]
        total = sum(d * w for d, w in zip(digits[:9], weights))
        checksum = total % 11
        if checksum == 10:
            checksum = 0

        return checksum == digits[9]


    def find(self, doc: str) -> Iterable[PiiEntity]:
        # RNO
        for item in self.rno_pattern.finditer(doc):
            item_value = item.group()
            if self.validate(item_value):
                yield PiiEntity(
                    PiiEnum.GOV_ID,
                    item.start(),
                    item_value,
                    country=self.country,
                    name="Ukrainian RNO",
                )

# Task descriptor
PII_TASKS = [(PiiEnum.GOV_ID, UkrainianRNO)]