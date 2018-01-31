import copy

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse, NoReverseMatch

from .utils import get_callable

from django.conf import settings

from django.forms.widgets import Media, MediaDefiningClass
from django.utils.safestring import mark_safe

from django.utils.html import conditional_escape, html_safe, format_html

from .items import URL, SubMenu, Separator
from .boundhandler import BoundHandler
from .handlers import ItemHandler, URLHandler
from .itemview import SeparatorView, URLView


#! media
#! handle empty menus?
#! 'active' not enabled
#! icon_ref
#! disabled
#! expanded/disabled on whole menus as option
#! Separator is a LI item? But that is excessive and makes styling hard.
# what does Spec say?
#! item attrs
#! attrs shoud be default, if not item overriden?
#! since template filters only take one parameter, namespacing, or auto-app detection?
#! Needs attrs?
#class Menu(MediaDefiningClass):
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

    def __init__(self, request, menu=None, empty_permitted=False, attrs={}):
        self.request = request
        print('..........request:')
        print(str(request))
        self.path = ''
        self.menu = [] if menu is None else menu
        self.bound_menu = []
        self.empty_permitted = empty_permitted
        self.attrs.update(attrs)

 
    #! temp, until we get some definitions going
    def dispatch(self, menu_item_data):
        if (isinstance(menu_item_data, Separator)):
          return BoundHandler(
            self,
            ItemHandler(SeparatorView),
            menu_item_data
            )
        elif (isinstance(menu_item_data, SubMenu)): 
          return BoundHandler(
            self,
            URLHandler(URLView),
            menu_item_data
            )
        elif (isinstance(menu_item_data, URL)):
          return BoundHandler(
            self,
            URLHandler(URLView),
            menu_item_data
            )
      
      
    #! test 'active'
    def _html_output_recursive(self, b, menu, 
        menu_start, 
        menu_end, 
        item_start,
        item_end
    ):
        '''
        Output HTML.
        Construct the surrounding HTML framework for items.
        Used by as_table(), as_ul(), as_p().
        '''
        #? extra classes: selected, expanded, disabled?, submenu  
        # so triggered by  selected, expanded,
        # use bound_menu
        for bf in menu:
            #print('rend:')
            #print(str(e))
            html_class_attr = ''

            #bf = self.dispatch(item)
            #bf.is_hidden = True
            #bf.is_disabled = True
            css_classes = bf.css_classes()
            if css_classes:
                html_class_attr = ' class="%s"' % css_classes

            if (bf.wrap):
                b.append(item_start.format(attrs=html_class_attr))

            b.append(str(bf))
                                                
            #if (isinstance(item, SubMenu)):
            if (hasattr(bf, 'submenu') and bf.submenu):
                b.append(menu_start)
                self._html_output_recursive(b, bf.submenu,
                    menu_start,
                    menu_end,
                    item_start,
                    item_end
                )
                b.append(menu_end)

            if (bf.wrap):
                b.append(item_end)

    def _html_output(self, menu_start, menu_end, item_start, item_end):
        b = []
        # late. Protect?
        self.validate()
        #self._html_output_recursive(b, self.menu, 
        self._html_output_recursive(b, self.bound_menu, 
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

    def _validate_recursive(self, menu, bound_menu):
        for item in menu:
            bf = self.dispatch(item)
            bound_menu.append(bf)
            if (hasattr(item, 'submenu') and item.submenu):
                self._validate_recursive(item.submenu, bf.submenu)

    #like def full_clean(self):
    #! called where? errors < is_valid < [user control]
    def validate(self):
        """
        Run validations.
        Also generates boundfields.
        Also build menu wide data such as marking descendant hide or 
        disable.
        """
        self._validate_recursive(self.menu, self.bound_menu) 
        # like _clean_fields
        #for item in self.menu:
            # must get right handler (or create boundhandler?)
            #h =
            # now clean the data
            #data = h.clean(item)
            # the original loads errors, but should we tweak
            # boundhandlers (e.g. is_disabled = True)?
            #pass
