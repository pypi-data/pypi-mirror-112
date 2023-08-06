from typing import Optional, Sequence, Set, TYPE_CHECKING

from .scopes import ScopeDomain

if TYPE_CHECKING:
    from django.contrib.auth.models import PermissionsMixin


__all__ = 'user_checker',


def user_checker(
    check_scopes: Set[ScopeDomain],
    user: Sequence['PermissionsMixin'] = None,
    obj: Optional[object] = None,
    **kwargs
) -> bool:
    """User scopes checker."""

    return (
        False if user is None else
        True if not check_scopes or len(check_scopes) == 0 else
        any(user.has_perm(scope, obj=obj) for scope in check_scopes)
    )
