from backend.app.core.roles import Role
from backend.app.core.permissions import Permission


ROLE_PERMISSIONS = {
    Role.ADMIN: {
        Permission.USERS_CREATE,
        Permission.USERS_READ,
        Permission.USERS_UPDATE,
        Permission.USERS_DELETE,

        Permission.DOCUMENTS_CREATE,
        Permission.DOCUMENTS_READ,
        Permission.DOCUMENTS_UPDATE,
        Permission.DOCUMENTS_DELETE,

        Permission.TICKETS_CREATE,
        Permission.TICKETS_READ,
        Permission.TICKETS_ASSIGN,
        Permission.TICKETS_UPDATE,
        Permission.TICKETS_RESOLVE,

        Permission.KNOWLEDGE_QUERY,
    },

    Role.MANAGER: {
        Permission.USERS_READ,

        Permission.DOCUMENTS_CREATE,
        Permission.DOCUMENTS_READ,
        Permission.DOCUMENTS_UPDATE,
        Permission.DOCUMENTS_DELETE,

        Permission.TICKETS_READ,
        Permission.TICKETS_ASSIGN,
        Permission.TICKETS_UPDATE,
        Permission.TICKETS_RESOLVE,

        Permission.KNOWLEDGE_QUERY,
    },

    Role.AGENT: {
        Permission.DOCUMENTS_READ,

        Permission.TICKETS_CREATE,
        Permission.TICKETS_READ,
        Permission.TICKETS_UPDATE,
        Permission.TICKETS_RESOLVE,

        Permission.KNOWLEDGE_QUERY,
    },

    Role.USER: {
        Permission.TICKETS_CREATE,
        Permission.TICKETS_READ,

        Permission.KNOWLEDGE_QUERY,
    },
}



def has_permission(role: Role | str, permission: Permission) -> bool:
    try:
        role = Role(role)
    except ValueError:
        return False

    permissions = ROLE_PERMISSIONS.get(role, set())

    return permission in permissions
