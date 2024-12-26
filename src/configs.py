from enum import Enum


class Extensions(Enum):
    PDF = "application/pdf"

    def __str__(self):
        return self.value
