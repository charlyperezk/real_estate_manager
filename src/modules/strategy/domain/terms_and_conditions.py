from typing import List
from dataclasses import dataclass, field
from src.seedwork.domain.mixins import check_rule
from .value_objects.term import Term, TermType, TermIdentifier
from .exceptions import TermNotFound
from .rules import TermTypeMustNotAlreadyBeInTerms

def auto_refresh_terms(method):
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self.refresh_registered_terms_quantity()
        return result
    return wrapper

@dataclass
class TermsAndConditions:
    terms: List[Term] = field(default_factory=list)
    registered_terms: int = 0
    
    def refresh_registered_terms_quantity(self) -> None:
        self.registered_terms = len(self.get_terms())

    @auto_refresh_terms
    def register_term(self, term: Term) -> None:
        check_rule(TermTypeMustNotAlreadyBeInTerms(identifier=term.type, terms=self.terms))
        self.terms.append(term)

    @auto_refresh_terms
    def unregister_term(self, term_type: TermIdentifier) -> None:
        term_founded = self.get_term_by_type(term_type)
        self.terms = [term_founded.deactivated() if term.type == term_type else term for term in self.terms]

    @auto_refresh_terms
    def delete_term(self, term_type: TermIdentifier) -> None:
        term_founded = self.get_term_by_type(term_type)
        self.terms = [term for term in self.terms if term.type != term_founded.type ]

    @auto_refresh_terms
    def update_term(self, term_type: TermIdentifier, **kwargs) -> None:
        term_founded = self.get_term_by_type(term_type)
        self.terms = [term_founded.with_main_attributes_updated(**kwargs) if term.type == term_type else term for term in self.terms]

    def get_terms(self, exclude_inactive=True) -> List[Term]:
        if not exclude_inactive:
            return self.terms
        else:
            return [term for term in self.terms if term.active]

    def get_term_by_type(self, term_type: TermIdentifier) -> Term:
        try:
            return next((term for term in self.terms if term == term_type))
        except StopIteration:
            raise TermNotFound(f"Can't found term {term_type} in terms")