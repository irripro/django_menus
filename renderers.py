
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, html_safe, format_html


from importlib import import_module

from django.conf import settings
#from .utils import get_menu_from_apps
from . import defaults

from django.core.exceptions import ImproperlyConfigured


MENU_DICT = ".menus.MENUS"

#! need an all(), cached
#? lazy data gathering, to cache
#! recursion here
#? API needs multiple query, so not stock map API?
#? but if recursion ok, stock map...
#? use attributes, not string keys
class MenuManager():
  
    def __init__(self):
        super().__init__()
        
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
    
    def get_menu_from_apps(self, menu_name):
        """
        Returns a consumable menulist for a given menu_name found in each menus.py file (if exists) on each app on
        INSTALLED_APPS
        :param menu_name: String, name of the menu to be found
        :return: Consumable menu list
        """
        installed_apps = getattr(settings, "INSTALLED_APPS", [])
        menu_list = []
        for app in installed_apps:
            try:
                #print(str(app + MENU_DICT))
                all_menus_dict = self.get_callable(app + MENU_DICT)
            except ImportError:
                all_menus_dict = None
            except AttributeError:
                all_menus_dict = None
            if all_menus_dict:
                menu_list += all_menus_dict.get(menu_name, [])
        return menu_list
    
    def get_menu(self, menu_name):
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
        menu_list = getattr(settings, menu_name, defaults.MENU_NOT_FOUND)
        menu_from_apps = self.get_menu_from_apps(menu_name)
        # If there isn't a menu on settings but there is menu from apps we built menu from apps
        if menu_list == defaults.MENU_NOT_FOUND and menu_from_apps:
            menu_list = menu_from_apps
        # It there is a menu on settings and also on apps we merge both menus
        elif menu_list != defaults.MENU_NOT_FOUND and menu_from_apps:
            #! this error could be static checked
            menu_list += menu_from_apps
            raise ImproperlyConfigured('A menu name in Settings is the same as a menu name in an application: menu name:{}: application{}'.format(
            menu_name,
            'TODO: this app name'
            ))
        #print(str(menu_list))
        #return generate_menu(context['request'], menu_list)
        #visible_menu = generate_menu(context['request'], menu_list)
        return menu_list


#MenuSet    
#! rename menurenderer
class MenuRenderer2():
   pass
        
class MenuRenderer:
    entries = {}
    template = None
    attrs = {}
    _built_attrs = ''
    _css_classes = ''
    
    def __init__(self, entries, attrs={}):
        self.entries = entries
        css_classes = attrs.pop('class', None)
        if (css_classes):
          self._css_classes = ' '.join(css_classes)
        if (not attrs):
            attrs = self.attrs
        self._built_attrs =  self._build_attrs(attrs)


    
    def _build_attrs(self, attrs):
        b = []         
        for k,v in attrs.items():
            b.append('{0}="{1}"'.format(k, v))
        return ' '.join(b)
        
    #! test 'active'
    def _html_output(self, row_tmpl):
        "Output HTML. Used by as_table(), as_ul(), as_p()."
        b = []
        for e in self.entries:
             print('rend:')
             print(str(e))
             attrs = self._built_attrs
             css_classes = 'class="{}{}"'.format(
                 self._css_classes,
                 ' active' if (e['selected']) else ''
             )
             entry_str = format_html(row_tmpl,
                 attrs= attrs,
                 icon= e['icon_class'],
                 url= e['url'],
                 name= e['name']
             )             
             b.append(entry_str)

        return mark_safe('\n'.join(b))

    def as_ul(self):
        "Return this menu rendered as HTML <li>s -- excluding the <ul></ul>."
        return self._html_output(
            row_tmpl='<li {attrs}>{icon}<a href="{url}">{name}</a></li>',
            )

    def as_div(self):
        "Return this menu rendered as HTML <div>s -- excluding a wrapping <div></div>."
        return self._html_output(
            row_tmpl='<div {attrs}>{icon}<a href="{url}">{name}</a></div>',
            )
            
    def __str__(self):
        return self.as_ul()

    def __repr__(self):
        return '<%(cls)>' % {
            'cls': self.__class__.__name__,
            #'valid': is_valid,
            #'fields': ';'.join(self.fields),
        }
