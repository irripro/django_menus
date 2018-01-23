import copy

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse, NoReverseMatch

from .utils import get_callable

from django.conf import settings

from django.forms.widgets import Media #, MediaDefiningClass
from django.utils.safestring import mark_safe

from django.utils.html import conditional_escape, html_safe, format_html

from .items import URL, SubMenu, Separator

#! rethink HTML
#! build basic CSS
#! media
#! 'active' not enabled
#! icon_ref
#! disabled
#! Separator
#! item attrs
#! attrs shoud be default, if not item overriden?
#! since template filters only take one parameter, namespacing, or auto-app detection?
class Menu():
    """
    Base class that generates menu list.
    
    @param attrs to add to menu items
    @param data [{menu item}, ...]
    """
    #? maybe for submenus also
    media = Media(
        css = {'all':'/django_menus/dropdown.css'}
    )
    attrs = {}
    _built_attrs = ''
    _css_classes = ''

    def __init__(self, menu=None, empty_permitted=False, attrs={}):
        self.path = ''
        self.request = None
        self.menu = [] if menu is None else menu
        self.empty_permitted = empty_permitted
        css_classes = attrs.pop('class', None)
        if (css_classes):
            if (self._css_classes):
                self._css_classes = self._css_classes + ' ' + css_classes
            else:
                self._css_classes = css_classes
              
        if (not attrs):
            #! chain
            attrs = self.attrs
        self._built_attrs =  self._build_attrs(attrs)

    #def clean(self):
        #for e in menu:
            #if (isinstance(e, URL)):
                #e.clean()

    def _build_attrs(self, attrs):
        b = []         
        for k,v in attrs.items():
            b.append('{0}="{1}"'.format(k, v))
        return ' '.join(b)
        
    def _rend_css_classes(self, extra_class_names=''):
        if (self._css_classes and extra_class_names):
            extra_class_names = ' ' + extra_class_names
        return 'class="{}{}"'.format(self._css_classes, extra_class_names)
                
    #! test 'active'
    def _html_output_recursive(self, b, menu, row_tmpl, menu_start, menu_end):
        "Output HTML. Used by as_table(), as_ul(), as_p()."
        for e in menu:
            print('rend:')
            print(str(e))

            if (isinstance(e, Separator)):
                b.append('<hr/>')
            elif (isinstance(e, SubMenu)):
                icon = '' 
                if (e.icon_ref is not None):
                    icon = '<img class="menu-item-icon" src="{}" />'.format(
                    e.icon_ref
                    )
                submenu_icon = '' 
                if (e.icon_submenu_ref is not None):
                    submenu_icon = '<img class="menu-submenu-icon" src="{}" />'.format(
                    e.icon_submenu_ref
                    )
                open_row_tmpl='<li {attrs}>{icon}<a href="{url}">{name}{submenu_icon}</a>'
                entry_str = open_row_tmpl.format(
                   attrs = self._built_attrs + self._rend_css_classes(),
                   icon = icon,
                   url = e.url,
                   submenu_icon = submenu_icon,
                   name = conditional_escape(e.name),
                )                  
                b.append(entry_str)                        
                b.append(menu_start)
                self._html_output_recursive(b, e.submenu, row_tmpl, menu_start, menu_end)
                b.append(menu_end)
                b.append('</li>')
            elif (isinstance(e, URL)):
                icon = '' 
                if (e.icon_ref is not None):
                    icon = '<img class="menu-item-icon" src="{}" />'.format(
                    e.icon_ref
                    )
                e.clean()
                if (not e.valid):
                    css_classes = 'class="{}{}"'.format(
                       self._css_classes,
                       ' disabled'
                    )
                    entry_str = '<li {attrs}>{icon}{name}</li>'.format(
                       attrs = self._built_attrs + css_classes,
                       icon = icon,
                       name = conditional_escape(e.name),
                    ) 

                    b.append(entry_str)                        
                else:
                    css_classes = 'class="{}{}"'.format(
                       self._css_classes,
                       ' active' # if (e['selected']) else ''
                    )
                    entry_str = row_tmpl.format(
                       attrs = self._built_attrs + css_classes,
                       icon = icon,
                       url = e.clean_url,
                       name = conditional_escape(e.name)
                    )             
                    print('entry_str:')
                    print(str(entry_str))
                    b.append(entry_str)

    def _html_output(self, row_tmpl, menu_start, menu_end):
        b = []
        self._html_output_recursive(b, self.menu, row_tmpl, menu_start, menu_end)
        return mark_safe('\n'.join(b))

    def as_ul(self):
        "Return this menu rendered as HTML <li>s -- excluding the <ul></ul>."
        return self._html_output(
            row_tmpl='<li {attrs}>{icon}<a href="{url}">{name}</a></li>',
            menu_start = '<ul>',
            menu_end = '</ul>'
            )

    def as_div(self):
        "Return this menu rendered as HTML <div>s -- excluding a wrapping <div></div>."
        return self._html_output(
            row_tmpl='<div {attrs}>{icon}<a href="{url}">{name}</a></div>',
            menu_start = '<div class="submenu">',
            menu_end = '</div>'
            )
            
    def __str__(self):
        return self.as_ul()

    def __repr__(self):
        return '<{}>'.format(
            self.__class__.__name__,
            #'valid': is_valid,
            #'menu': ';'.join(self.fields),
        )
    @property
    def media(self):
        """Return all media required to render the items on this menu."""
        media = self.media
        for e in self.menu:
            media = media + e.media
        return media
