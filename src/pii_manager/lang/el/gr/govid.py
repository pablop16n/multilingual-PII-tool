"""
Greek Goverment-issued IDs:
  - ADT (Αριθμός Ταυτότητας)
  - PA (Личен номер на чужденец)
"""

import re

from typing import Iterable


from pii_manager import PiiEnum, PiiEntity
from pii_manager.helper import BasePiiTask

# regex for ADT
_ADT_PATTERN = r"\b([Α-Ω]|[A-Z]){1,2}\s?\d{6}\b"
# regex for PA
_PA_PATTERN = r"\b(?=[A-Z0-9]{12}\b)(?=.*\d)[A-Z0-9]{12}\b"



class GreekAdtPa(BasePiiTask):
    """
    Greek Government-issued ADT and PA numbers, recognize & validate
    """

    pii_name = "Greek ADT/PA"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Compile the regex
        self.adt_pattern = re.compile(_ADT_PATTERN, flags=re.X)
        self.pa_pattern = re.compile(_PA_PATTERN, flags=re.X)

    def find(self, doc: str) -> Iterable[PiiEntity]:
        # ADT
        for item in self.adt_pattern.finditer(doc):
            item_value = item.group()
            yield PiiEntity(
                PiiEnum.GOV_ID,
                item.start(),
                item_value,
                country=self.country,
                name=" Greek ADT",
            )

        # PA
        for item in self.pa_pattern.finditer(doc):
            item_value = item.group()
            yield PiiEntity(
                PiiEnum.GOV_ID,
                item.start(),
                item_value,
                country=self.country,
                name=" Greek PA",
            )
# Task descriptor
PII_TASKS = [(PiiEnum.GOV_ID, GreekAdtPa)]