"""
Canadian license plate
"""

import re

from typing import Iterable


from pii_manager import PiiEnum, PiiEntity
from pii_manager.helper import BasePiiTask

# regex for license plate
_LICENSE_PLATE_PATTERN = r"\b[A-Z0-9]{5,7}\b"
_REGIONAL_PLATE_PATTERN = r"\b([A-Z]{3}-?\d{4}|\d{3}\s?[A-Z]{3}|[A-Z]{2}\d\s?\d{2}[A-Z]|[A-Z]{3}\s?\d{3}|[A-Z]{3}-?\d{3}|[A-Z]{3}\s?\d{2}|\d{5}|\d{3}\s?\d{3})\b"



class CanadianLicensePlate(BasePiiTask):
    """
    Canadian license plate numbers recognize
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Compile the regex
        self.license_plate_pattern = re.compile(_LICENSE_PLATE_PATTERN, flags=re.X | re.IGNORECASE)

    def find(self, doc: str) -> Iterable[PiiEntity]:
        # license plate
        for item in self.license_plate_pattern.finditer(doc):
            item_value = item.group()
            if not re.match(_REGIONAL_PLATE_PATTERN, item_value):
                continue
            yield PiiEntity(
                PiiEnum.LICENSE_PLATE,
                item.start(),
                item_value,
                country=self.country,
                name="Canadian license plate",
            )
# Task descriptor
PII_TASKS = [(PiiEnum.LICENSE_PLATE, CanadianLicensePlate)]