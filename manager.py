
from importlib import import_module
from django.conf import settings

from .items import SubMenu

MENU_DICT = ".menubase.MENUS"


#! need an all(), cached
#? lazy data gathering, to cache
#? API needs multiple query, so not stock map API?
#? but if recursion ok, stash map...
#? use attributes, not string keys
class MenuManager():
    all_app_menus = {}
    
    def __init__(self):
        self.load_app_menus()
        #super().__init__()
        
    def get_callable(self, func_or_path):
        """
        Receives a dotted path or a callable, Returns a callable or None
        """
        if callable(func_or_path):
            return func_or_path
    
        module_name = '.'.join(func_or_path.split('.')[:-1])
        function_name = func_or_path.split('.')[-1]
        _module = import_module(module_name)
        func = getattr(_module, function_name)
        return func

    def load_app_menus(self):
        installed_apps = getattr(settings, "INSTALLED_APPS", [])
        for app in installed_apps:
            try:
                app_menus = self.get_callable(app + MENU_DICT)
            except ImportError:
                app_menus = None
            except AttributeError:
                app_menus = None
            if app_menus:
                 self.all_app_menus[app] = app_menus

    def load_menu(self, app, menu_name):
        return self.all_app_menus[app][menu_name]

    def _call_recursive(self, app, menu_name):
        menu = self.load_menu(app, menu_name)
        for idx, e in enumerate(menu):
             if (isinstance(e, SubMenu)):
                 submenu = self._call_recursive(app, e.menu_ref)
                 menu[idx].submenu = submenu
        return menu
        
    def __call__(self, app, menu_name):
        return self._call_recursive(app, menu_name)
        
    def get(self, app, menu_name):
        """
        Get menu data.
        
        @return if fails, return empty list
        """
        r = None
        try:
            r = self(app, menu_name)
        except KeyError:
            pass        
        return r
        
    def get_menus(self, app, menu_names):
        """
        Get data from several menus.
        
        @param menu_names iterable of menu names
        @return if fails, return empty list
        """
        if (not app in self.all_app_menus):
            return None
        return {mn:get(app, mn) for mn in menu_names}
            
    def __str__(self):
        return '<{}>'.format(
            self.__class__.__name__
            )

    def __repr__(self):
        b = []
        for app_name, v in self.all_app_menus.items():
            for menu_name in v.keys():
                b.append('{}->{}'.format(app_name, menu_name))
        menus = ';'.join(b)
        
        return '<{} menus:{}>'.format(
            self.__class__.__name__,
            menus,
        )
