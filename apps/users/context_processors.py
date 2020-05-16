from .utils import *

def user_roles(request):
    context = {}
    if request.user.is_authenticated:
        context['is_administrator'] = request.user.profile.user_type.code == 1
        can_read, can_write = user_permissions(request.user)
        context['can_read'] = can_read
        context['can_write'] = can_write
        context['user_type_code'] = request.user.profile.user_type.code 
    return context