from typing import Any, Dict


class IncorrectExtension(Exception):
    message: str = "Invalid Document Type"

    def __init__(self, details: Dict[str, Any]) -> None:
        self._details = details

    def details(self) -> Dict[str, Any]:
        return self._details
