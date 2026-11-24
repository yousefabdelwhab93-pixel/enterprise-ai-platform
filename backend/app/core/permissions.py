from enum import StrEnum


class Permission(StrEnum):
    # Users
    USERS_CREATE = "users:create"
    USERS_READ = "users:read"
    USERS_UPDATE = "users:update"
    USERS_DELETE = "users:delete"

    # Documents
    DOCUMENTS_CREATE = "documents:create"
    DOCUMENTS_READ = "documents:read"
    DOCUMENTS_UPDATE = "documents:update"
    DOCUMENTS_DELETE = "documents:delete"

    # Tickets
    TICKETS_CREATE = "tickets:create"
    TICKETS_READ = "tickets:read"
    TICKETS_ASSIGN = "tickets:assign"
    TICKETS_UPDATE = "tickets:update"
    TICKETS_RESOLVE = "tickets:resolve"

    # Knowledge Base
    KNOWLEDGE_QUERY = "knowledge:query"