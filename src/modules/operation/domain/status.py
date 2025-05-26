from enum import Enum

class OperationStatus(str, Enum):
    PAID = "paid"
    IN_PROGRESS = "in_progress"
    ACTIVE = "active"
    UNDER_REVIEW = "under_review"
    CANCELLED = "cancelled"