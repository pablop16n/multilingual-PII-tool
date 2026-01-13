"""
Peruvian Government-issued IDs:
  - DNI (Documento Nacional de Identidad)
"""

import re

from typing import Iterable

from stdnum.pe import cui

from pii_manager import PiiEnum, PiiEntity
from pii_manager.helper import BasePiiTask

# regex for CUI
_CUI_PATTERN = r"\b\d{8}\b"


class PeruvianCUI(BasePiiTask):
    """
    Peruvian Government-issued CUI numbers, recognize & validate
    """

    pii_name = "Peruvian CUI"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Compile the regex
        self.cui_pattern = re.compile(_CUI_PATTERN, flags=re.X)


    def find(self, doc: str) -> Iterable[PiiEntity]:
        # CUI
        for item in self.cui_pattern.finditer(doc):
            item_value = item.group()
            if cui.is_valid(item_value):
                yield PiiEntity(
                    PiiEnum.GOV_ID,
                    item.start(),
                    item_value,
                    country=self.country,
                    name="Peruvian CUI",
                )

# Task descriptor
PII_TASKS = [(PiiEnum.GOV_ID, PeruvianCUI)]