import copy

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse, NoReverseMatch

from .utils import get_callable

from django.conf import settings

from django.forms.widgets import Media #, MediaDefiningClass
from django.utils.safestring import mark_safe

from django.utils.html import conditional_escape, html_safe, format_html

from .items import URL, SubMenu, Separator

#! media
#! 'active' not enabled
#? theres a difference between 'hover/link/active/visited' and 'currently selected'.
#? Do we want 'currently selected' at all? What's web 'active'?
#! icon_ref
#! disabled
#! expanded/disabled on whole menus as option
#! Separator is a LI item?
#! item attrs
#! attrs shoud be default, if not item overriden?
#! since template filters only take one parameter, namespacing, or auto-app detection?
#? expanded Drupal-like theme
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

    def __init__(self, request, menu=None, empty_permitted=False, attrs={}):
        self.request = request
        print('..........request:')
        print(str(request))
        self.path = ''
        self.menu = [] if menu is None else menu
        self.empty_permitted = empty_permitted
        css_classes = attrs.pop('class', None)
        if (css_classes):
            if (self._css_classes):
                self._css_classes = self._css_classes + ' ' + css_classes
            else:
                self._css_classes = css_classes

        self.attrs.update(attrs)

    
    def _build_attrs(self, attrs):
        b = []         
        for k,v in attrs.items():
            b.append('{0}="{1}"'.format(k, v))
        return ' '.join(b)
    
    #! if classes is empty string?    
    def _rend_attrs(self, menu_item):
        classes = []
        if (menu_item.selected):
            classes.append('selected') 
        if (menu_item.expanded):
            classes.append('expanded')
        if (menu_item.disabled):
            classes.append('disabled')
        classes.append(menu_item.wrap_css_classes) 

        if (classes):
            local_classes = self.attrs.get('class')
            if (local_classes):
                classes.append(local_classes)
            attrs = self.attrs.copy()
            attrs['class'] = ' '.join(classes)
        return self._build_attrs(attrs)

                                    
    #! test 'active'
    def _html_output_recursive(self, b, menu, 
        menu_start, 
        menu_end, 
        item_start,
        item_end
    ):
        "Output HTML. Used by as_table(), as_ul(), as_p()."
        #? extra classes: selected, expanded, disabled?, submenu  
        # so triggered by  selected, expanded,
        for e in menu:
            #print('rend:')
            #print(str(e))

            if (isinstance(e, Separator)):
                #print('rend Separator:')
                b.append(e.render(self.request))
            elif (isinstance(e, SubMenu)): 
                e.clean()
                b.append(item_start.format(attrs = self._rend_attrs(e)))
                b.append(e.render(self.request))
                b.append(menu_start)
                self._html_output_recursive(b, e.submenu,
                    menu_start,
                    menu_end,
                    item_start,
                    item_end
                )
                b.append(menu_end)
                b.append(item_end)
            elif (isinstance(e, URL)):
                #! in items
                e.clean()
                if (not e.valid):
                    #? This gear should be in the item
                    css_classes = 'class="{}{}"'.format(
                       self._css_classes,
                       ' disabled'
                    )
                    b.append(item_start.format(attrs = self._rend_attrs(e)))
                    b.append(e.render(self.request))
                    b.append(entry_str)                        
                else:
                    #? This gear should be in the item
                    css_classes = 'class="{}{}"'.format(
                       self._css_classes,
                       ' active' # if (e['selected']) else ''
                    )
                    b.append(item_start.format(attrs = self._rend_attrs(e)))
                    b.append(e.render(self.request))
                    b.append(item_end)

    def _html_output(self, menu_start, menu_end, item_start, item_end):
        b = []
        self._html_output_recursive(b, self.menu, 
        menu_start, 
        menu_end,
        item_start,
        item_end
        )
        return mark_safe(''.join(b))

    def as_ul(self):
        "Return this menu rendered as HTML <li>s -- excluding the <ul></ul>."
        return self._html_output(
            menu_start = '<ul>',
            menu_end = '</ul>',
            item_start = '<li {attrs}>',
            item_end = '</li>'
            )

    def as_div(self):
        "Return this menu rendered as HTML <div>s -- excluding a wrapping <div></div>."
        return self._html_output(
            menu_start = '<div class="submenu">',
            menu_end = '</div>',
            item_start = '<div {attrs}>',
            item_end = '</div>'
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
