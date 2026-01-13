"""
Cuban Government-issued IDs:
  - NI (Número de identidad)
"""

import re

from typing import Iterable

from stdnum.cu import ni

from pii_manager import PiiEnum, PiiEntity
from pii_manager.helper import BasePiiTask

# regex for NI
_NI_PATTERN = r"\b\d{8}\b"


class CubanNI(BasePiiTask):
    """
    Cuban Government-issued NI numbers, recognize & validate
    """

    pii_name = "Cuban NI"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Compile the regex
        self.ni_pattern = re.compile(_NI_PATTERN, flags=re.X)


    def find(self, doc: str) -> Iterable[PiiEntity]:
        # NI
        for item in self.ni_pattern.finditer(doc):
            item_value = item.group()
            if ni.is_valid(item_value):
                yield PiiEntity(
                    PiiEnum.GOV_ID,
                    item.start(),
                    item_value,
                    country=self.country,
                    name="Cuban NI",
                )

# Task descriptor
PII_TASKS = [(PiiEnum.GOV_ID, CubanNI)]