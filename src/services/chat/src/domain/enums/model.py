from enum import StrEnum
from typing import List


# add other models later
class Model(StrEnum):
    GEMINI = "gemini"
    GPT = "gpt"

    @property
    def values() -> List[str]:
        return [model.value for model in Model]
