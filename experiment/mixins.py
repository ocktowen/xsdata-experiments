from typing import Any


class XMLDummyMixin:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        print("XMLDummyMixin init called")
        super().__init__(*args, **kwargs)
