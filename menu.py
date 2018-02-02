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



class DeclarativeFieldsMetaclass(MediaDefiningClass):
    """Collect Fields declared on the base classes."""
    def __new__(mcs, name, bases, attrs):
        # Collect fields from current class.
        current_fields = []
        for key, value in list(attrs.items()):
            if isinstance(value, Handler):
                current_fields.append((key, value))
                attrs.pop(key)
        attrs['declared_fields'] = OrderedDict(current_fields)

        new_class = super(DeclarativeFieldsMetaclass, mcs).__new__(mcs, name, bases, attrs)

        # Walk through the MRO.
        declared_fields = OrderedDict()
        for base in reversed(new_class.__mro__):
            # Collect fields from base class.
            if hasattr(base, 'declared_fields'):
                declared_fields.update(base.declared_fields)

            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_fields:
                    declared_fields.pop(attr)

        new_class.base_fields = declared_fields
        new_class.declared_fields = declared_fields

        return new_class

    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        # Remember the order in which form fields are defined.
        return OrderedDict()
        
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
    
    @param menu [{menu item}, ...]
    @param attrs to add to menu items
    """
    # unmutable
    #? maybe for submenus also
    media = Media(
        css = {'all':'/django_menus/dropdown.css'}
    )
    #disable_invalid_items = False
    disable_invalid_items = True
    attrs = {}
    
    
    def __init__(self, request, menu=None, disable_invalid=None, attrs={}):
        self.request = request
        #print('..........request:')
        #print(str(request))
        self.path = ''
        # copy to prevent changing the original
        self.menu = [] if menu is None else copy.deepcopy(menu)
        self.bound_menu = []
        if disable_invalid is not None:
            self.disable_invalid = disable_invalid
        self.attrs.update(attrs)
        self.validate()
 
    #! temp, until we get some definitions going
    def dispatch(self, menu_item_data):
        if (isinstance(menu_item_data, Separator)):
          return BoundHandler(
            ItemHandler(SeparatorView),
            menu_item_data
            )
        elif (isinstance(menu_item_data, SubMenu)): 
          return BoundHandler(
            URLHandler(URLView),
            menu_item_data
            )
        elif (isinstance(menu_item_data, URL)):
          return BoundHandler(
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
        visible_count = 0
        #? extra classes: selected, expanded, disabled?, submenu  
        # so triggered by  selected, expanded,
        # use bound_menu
        for bh in menu:
            print('rend:' + repr(bh))
            if (bh.is_valid or self.disable_invalid_items):
                visible_count += 1
                #if hasattr(bh.item_data, 'name'):
                    #print(str(bh.item_data.name) + ':'+ str(bh.is_valid))
                    #print('menu classes:' + bh.css_classes())
                html_class_attr = ''
    
                #bh = self.dispatch(item)
                #bh.is_valid = False
                css_classes = bh.css_classes()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes
    
                if (bh.wrap):
                    b.append(item_start.format(attrs=html_class_attr))
                b.append(str(bh))
                #if (isinstance(item, SubMenu)):
                if (hasattr(bh, 'submenu') and bh.submenu):
                    bsub = []
                    count = self._html_output_recursive(bsub, bh.submenu,
                        menu_start,
                        menu_end,
                        item_start,
                        item_end
                    )
                    if (count > 0):
                        b.append(menu_start)
                        b.extend(bsub)
                        b.append(menu_end)
                if (bh.wrap):
                    b.append(item_end)
        return visible_count
            
    def _html_output(self, menu_start, menu_end, item_start, item_end):
        b = []
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

    #! noit catching double layer invalid?
    def _validate_recursive(self, menu, bound_menu, menu_is_valid=True):
        for item in menu:
            bh = self.dispatch(item)
            item_is_valid = bh.validate(menu_is_valid)
            #test
            if (hasattr(item, 'name') and (item.name == 'Reviews')):
                bh.is_valid = False
                item_is_valid = False
            bound_menu.append(bh)
            #if hasattr(item, 'name'):
            #    print(str(item.name) + ':'+ str(bh.is_valid))
            if (hasattr(item, 'submenu') and item.submenu):
                self._validate_recursive(item.submenu, bh.submenu, item_is_valid)

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

