"""
Slovenian Government-issued IDs:
  - EMSO (Enotna matična številka občana)
"""

import re

from typing import Iterable

from stdnum.si import emso

from pii_manager import PiiEnum, PiiEntity
from pii_manager.helper import BasePiiTask

# regex for EMSO
_EMSO_PATTERN = r"\b(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])\d{3}(5[0-9])\d{3}\d\b"


class SlovenianEMSO(BasePiiTask):
    """
    Slovenian Government-issued EMSO numbers, recognize & validate
    """

    pii_name = "Slovenian EMSO"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Compile the regex
        self.emso_pattern = re.compile(_EMSO_PATTERN, flags=re.X)


    def find(self, doc: str) -> Iterable[PiiEntity]:
        # EMSO
        for item in self.emso_pattern.finditer(doc):
            item_value = item.group()
            if emso.is_valid(item_value):
                yield PiiEntity(
                    PiiEnum.GOV_ID,
                    item.start(),
                    item_value,
                    country=self.country,
                    name="Slovenian EMSO",
                )

# Task descriptor
PII_TASKS = [(PiiEnum.GOV_ID, SlovenianEMSO)]