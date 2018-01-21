
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
    #{app -> [menu_name -> data]}
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
    
    def get(self, app, menu_name):
        """
        Get menu data.
        
        @return if fails, return None
        """
        if (app in self.all_app_menus):
            return self.all_app_menus[app].get(menu_name)        

    def get_menus(self, app, menu_names):
        """
        Get data from several menus.
        
        @return if fails, return empty list
        """
        if (not app in self.all_app_menus):
            return []
        return {mn:self.all_app_menus[app][mn] for mn in self.all_app_menus[app].keys() if (mn in menu_names)}
            
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
