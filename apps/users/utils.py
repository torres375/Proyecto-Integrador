def user_permissions(user):
    profile = user.profile
    can_read = True
    can_write = write_permissions(user)
    return can_read, can_write


def read_permissions(user):
    has_permissions = False
    if user.is_authenticated:
        profile = user.profile
        has_permissions = True
    return has_permissions


def write_permissions(user):
    has_permissions = False
    if user.is_authenticated:
        profile = user.profile
        has_permissions = profile.user_type.code == 1 or profile.user_type.code == 4 or profile.user_type.code == 5 
    return has_permissions
