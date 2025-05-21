from typing import List, Union
from dataclasses import dataclass, field
from .value_objects.term import Term, TermType, TermIdentifier
from .exceptions import TermNotFound

@dataclass
class TermsAndConditions:
    terms: List[Term] = field(default_factory=list)
    registered_terms: int = 0
    
    def register_term(self, term: Term) -> None: #TODO: Check rules
        self.terms.append(term)
        self.registered_terms += 1

    def unregister_term(self, term_type: TermIdentifier) -> None: #TODO: Check rules
        self.terms = [term for term in self.terms if term.type != term_type]
        self.registered_terms -= 1
    
    def get_terms(self, exclude_inactive=False) -> List[Term]:
        if not exclude_inactive:
            return self.terms
        else:
            return [term for term in self.terms if term.active]

    def get_term_by_type(self, term_type: TermIdentifier) -> Term:
        try:
            return next((term for term in self.terms if term == term_type))
        except StopIteration:
            raise TermNotFound(f"Can't found term {term_type} in terms")