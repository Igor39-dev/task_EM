from .models import AccessRoleRule, UserRole


def check_permission(user, element_code, action, obj=None):
    role_ids = UserRole.objects.filter(
        user=user
    ).values_list('role_id', flat=True)

    rules = AccessRoleRule.objects.filter(
        role_id__in=role_ids,
        element__code=element_code
    )

    for r in rules:
        if action == 'read' and r.read_all_permission:
            return True

        if action == 'read' and r.read_permission and obj and obj.owner_id == user.id:
            return True

    return False
