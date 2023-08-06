from typing import List, Any

from pydantic import BaseModel


class Console(BaseModel):
    logs: List[Any] = []
    errors: List[Any] = []
    warnings: List[Any] = []

    def log(self, item):
        self.logs.append(item)

    def error(self, item):
        self.errors.append(item)

    def warning(self, item):
        self.warnings.append(item)
