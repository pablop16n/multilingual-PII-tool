"""
Cypriot Government-issued IDs:
  - KDT (Κυπριακό δελτίο ταυτότητας)
"""

import re

from typing import Iterable

from pii_manager import PiiEnum, PiiEntity
from pii_manager.helper import BasePiiTask

# regex for KDT
_KDT_PATTERN = r"\b[A-Z]\d{7}[A-Z]\b"


class CypriotKDT(BasePiiTask):
    """
    Cypriot Government-issued KDT numbers, recognize & validate
    """

    pii_name = "Cypriot KDT"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Compile the regex
        self.kdt_pattern = re.compile(_KDT_PATTERN, flags=re.X)


    def find(self, doc: str) -> Iterable[PiiEntity]:
        # KDT
        for item in self.kdt_pattern.finditer(doc):
            item_value = item.group()
            yield PiiEntity(
                PiiEnum.GOV_ID,
                item.start(),
                item_value,
                country=self.country,
                name="Cypriot KDT",
            )

# Task descriptor
PII_TASKS = [(PiiEnum.GOV_ID, CypriotKDT)]