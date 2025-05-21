from pydantic import BaseModel


class BusinessRule(BaseModel):
    """This is a base class for implementing domain rules"""

    class Config:
        arbitrary_types_allowed = True

    # This is an error message that broken rule reports back
    _message: str = "Business rule is broken"

    def get_message(self) -> str:
        return self._message

    def is_broken(self) -> bool:
        raise NotImplementedError("is_broken must be implemented")

    def __str__(self):
        return f"{self.__class__.__name__} {super().__str__()}"
