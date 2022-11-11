class QueryPriorityTypes:
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    CHOICES = [
        (HIGH, "high"),
        (MEDIUM, "medium"),
        (LOW, "low")
    ]

class QueryStatus:
    QUERY_RECEIVED = "query_received"
    QUERY_IN_PROGRESS = "query_in_progress"
    QUERY_RESOLVED = "query_resolved"
    QUERY_REJECTED = "query_rejected"

    CHOICES = [
        (QUERY_RECEIVED, "query_received"),
        (QUERY_IN_PROGRESS, "query_in_progress"),
        (QUERY_RESOLVED, "query_resolved"),
        (QUERY_REJECTED, "query_rejected")
    ]
