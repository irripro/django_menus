from django import template
from django.conf import settings

from .utils import get_menu_from_apps
from .. import defaults
from ..menu import generate_menu
from django.utils.safestring import mark_safe

from ..renderers import MenuRenderer
register = template.Library()

from ..manager import MenuManager
from ..menu_handler import Menu

# [{'url': '/app1-feature', 'submenu': None, 'icon_class': '', 'selected': False, 'name': 'App1 Feature'}, {'url': '/about', 'submenu': None, 'icon_class': '', 'selected': False, 'name': 'About'}]


@register.assignment_tag(takes_context=True)
def get_menu(context, menu_name):
    """
    Returns a consumable menu list for a given menu_name found in settings.py.
    Else it returns an empty list.

    Update, March 18 2017: Now the function get the menu list from settings and append more items if found on the
    menus.py's 'MENUS' dict.
    :param context: Template context
    :param menu_name: String, name of the menu to be found
    :return: Generated menu
    """
    print('......get_menu')

    #menu_list = getattr(settings, menu_name, defaults.MENU_NOT_FOUND)
    #menu_from_apps = get_menu_from_apps(menu_name)
    ## If there isn't a menu on settings but there is menu from apps we built menu from apps
    #if menu_list == defaults.MENU_NOT_FOUND and menu_from_apps:
        #menu_list = menu_from_apps
    ## It there is a menu on settings and also on apps we merge both menus
    #elif menu_list != defaults.MENU_NOT_FOUND and menu_from_apps:
        #menu_list += menu_from_apps
    ##print(str(menu_list))
    ##return generate_menu(context['request'], menu_list)
    #visible_menu = generate_menu(context['request'], menu_list)
    #return MenuRenderer(visible_menu).as_ul()
    a = MenuManager()
    md = a.get_recursive('filmstat', 'NAV_MENU_TOP')
    m = Menu(context.request, md)
    return str(m)

