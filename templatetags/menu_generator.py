from django import template
#from django.conf import settings

from django.core.exceptions import ImproperlyConfigured

register = template.Library()

from ..manager import MenuManager
from ..menu import Menu, EXACT, TAIL1, TAIL2, HEAD1, HEAD2



@register.assignment_tag(takes_context=True)
def get_menu(context, menu_url):
    """
    Returns menu HTML for a menu path to a configuration.
    The menu is currently pre-configured to expand and select.
    Else it returns an empty list?

    :param menu_name: Path of the menu to be found: app_name ~ '/' ~ menu_name ~ Optional('?' ~ OneOrMoreore(initkey ~ '=' ~ initValue ~ ';'))
    """
    s = menu_url.split('?', 1) 
    menu_path = s[0]
    menu_app, menu_name = menu_path.split('/', 1) 
    query = {}
    try:
        if (len(s) > 1):
          kvs = s[1].split(';')
          for kv in kvs:
            k, v = kv.split('=')
            if (v == 'False'):
                v = False
            if (v == 'True'):
                v = True
            if (v == 'EXACT'):
                v = EXACT
            if (v == 'TAIL1'):
                v = TAIL1
            if (v == 'TAIL2'):
                v = TAIL2
            if (v == 'HEAD1'):
                v = HEAD1
            if (v == 'HEAD2'):
                v = HEAD2
            query[k] = v 
    #print(menu_name + 'query:' + str(query))
    except Exception:
        raise ImproperlyConfigured('Django menu configuration URL can not be parsed: url:"{}"'.format(menu_url))
    m = Menu(context.request, menu_name, menu_app, **query)
    return str(m)

