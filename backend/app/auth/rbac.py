"""
JanSahay AI - Role-Based Access Control (RBAC)
Provides role-checking dependencies for API endpoints.
"""

from functools import wraps
from fastapi import Depends, HTTPException, status
from app.auth.oauth2 import require_auth
from app.models.user import User, UserRole


def require_role(*allowed_roles: UserRole):
    """Dependency that checks if the current user has one of the allowed roles."""
    async def role_checker(user: User = Depends(require_auth)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in allowed_roles]}"
            )
        return user
    return role_checker


# Convenience dependencies
require_admin = require_role(UserRole.ADMIN)
require_gov_official = require_role(UserRole.ADMIN, UserRole.GOV_OFFICIAL)
require_citizen = require_role(UserRole.CITIZEN, UserRole.ADMIN)
