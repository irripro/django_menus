from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



def is_authenticated(request, item_data):
    """
    True if request.user authenticated else False
    """
    if (not request.user.is_authenticated):
        raise ValidationError(_('Not authenticated.'), code='invalid')

def is_superuser(request, item_data):
    """
    True if request.user is superuser else False
    """
    if (not is_authenticated(request, item_data) and request.user.is_superuser):
        raise ValidationError(_('Not superuser.'), code='invalid')


def is_staff(request, item_data):
    """
    True if request.user is staff else False
    """
    if (not is_authenticated(request, item_data) and request.user.is_staff):
        raise ValidationError(_('Not staff.'), code='invalid')

def is_anonymous(request, item_data):
    """
    True if request.user is not authenticated else False
    """
    if (request.user.is_authenticated):
        raise ValidationError(_('User is not anonymous.'), code='invalid')

class PermissionValidator:
    def __init__(self, perm):
        self.perm = perm
        
    def __call__(self, request, item_data):
        if (not request.user.has_perm(self.perm)):
            raise ValidationError(
                _('User has no permission.'), 
                code='invalid',
                params={
                    'perm': self.perm,
                }
            )   
             
def has_permission(perm):
    """
    True if request.user is has permission else False
    """
    return PermissionValidator(perm)
