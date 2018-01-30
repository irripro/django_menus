#__author__ = 'Milton Lenis @ Rady Consultores'
#__description__ = 'A straightforward menu generator for Django'
__version__ = '1.0.2'

#default_app_config = 'menu_generator.apps.MenuAppConfig'

from .items import(
    SubMenu,
    URL,
    Separator
)

from .manager import(
    MenuManager
)

#from .menu_handler import (
#    Menu
#)

from .menu import (
    Menu
)
