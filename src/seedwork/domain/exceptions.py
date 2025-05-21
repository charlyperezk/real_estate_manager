from .rules import BusinessRule

class DomainException(Exception):
    pass


class BusinessRuleValidationException(DomainException):
    def __init__(self, rule: BusinessRule):
        self.rule = rule

    def __str__(self):
        return self.rule.get_message()


class EntityNotFoundException(Exception):
    def __init__(self, repository, **kwargs):

        message = f"Entity with {kwargs} not found"
        super().__init__(message)
        self.repository = repository
        self.kwargs = kwargs
