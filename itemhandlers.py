import itertools

from django.core.exceptions import ImproperlyConfigured
from django.forms.widgets import Media


from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.utils.html import conditional_escape, html_safe, format_html

from .itemview import ItemView, SeparatorView, URLView
from .boundhandler import BoundHandler


#? make a queryset version
#? include validators from items?
#? should allow configuration of attributes by item type?
# and even media?
class ItemHandler:
    '''
    Configuration and validation of item data.
    For each type of menu item, there is a handler. The handler contains
    configuration which is overall for the item. The configuration can 
    be set by the user.
    Handlers are constructed per menu, then cached across web calls. Added
    attributes should be regarded as as immutable, and the methods 
    as idempotent. 
    '''
    view = SeparatorView
    validators = []

    def __init__(self, 
        view=None,
        validators=()
        ):
        view = view or self.view
        if isinstance(view, type):
            view = view()
        else:
            view = copy.deepcopy(view)
            
        # handler-defined attrs.
        #? Not sure about this action. Let boundhandler, which also has 
        # view_attrs, do the job? It's not a big deal, is it?
        #extra_attrs = self.get_view_attrs(view)
        #if extra_attrs:
            #view.attrs.update(extra_attrs)
        self.view = view
        self.validators = list(itertools.chain(self.validators, validators))
        super().__init__()

    def prepare_item(self, item):
        '''
        Prepare input data for validation.
        If the data is normalised or some other mutation, then it must 
        be copied.
        '''
        return item
        
    def run_validators(self, request, item):
        validated = True
        for v in self.validators:
            #try:
                v(request, item)
            #except ValidationError as e:
            #    validated = False

    def validate(self, request, item):
        '''
        @return clean data
        @throw validation error
        '''
        item = self.prepare_item(item)
        self.run_validators(request, item)

    def get_view_attrs(self, view):
        """
        Given a View instance (*not* a View class), return a dictionary of
        any HTML attributes that should be added to the View, based on this
        Handler.
        """
        return {}
        
    def get_wrap_css_classes(self, finished_data):
        '''
        Add classes to the wrap.
        The method is supplied with the finished data. This has 
        extensions added and is is validated.
        '''
        return set()
        
    def extend_data(self, initial_ctx, menu, bound_handler, valid, trail=[]):
        '''
        Add data to extend the config data.
        When this data is requested, the configuration data is validated 
        and transformed into an initial_context.
        
        Unlike the handler data, which is cached and
        immutable, the extended data has been copied so can be modified 
        by other code in Boundhandler, Menu, etc. The values are then 
        used as a render context.
        
        This method can add immutable data from the handler to the 
        future context. It also recieves useful data,
        including the menu and bound handler which called it. So it can 
        react to information given, modifying the extended data
        by item type.
        '''
        pass
        
        
        
class SeparatorHandler(ItemHandler):
    pass
        
        
        
class URLHandler(ItemHandler):      
    view = URLView
        
    #? handy?
    def absolute_path(self, path):
        """
        Given a relative or absolute path to a static asset, return an absolute
        path. An absolute path will be returned unchanged while a relative path
        will be passed to django.templatetags.static.static().
        """
        if path.startswith(('http://', 'https://', '/')):
            return path
        return static(path)
        
    # What may need to be altered here?
    def prepare_data(self, data):
        #data[url] = absolute_path(data[url])
        return data
        
    def extend_data(self, initial_ctx, menu, bound_handler, valid, trail=[]):
        super().extend_data(initial_ctx, menu, valid, bound_handler, trail)
        initial_ctx.update({
        'selected': ((menu.select_trail or menu.select_leaf) and (bound_handler in trail)),
        'disabled': (not valid),
        })

    def get_wrap_css_classes(self, finished_data):
        classes = super().get_wrap_css_classes(finished_data)
        #print('self.is_expanded' + str(self.is_expanded))
        if (finished_data['selected']):
            classes.add('selected')
        if (finished_data['disabled']):
            classes.add('disabled')
        return classes        



class SubmenuHandler(URLHandler):
    def __init__(self, *,
        expanded=False,
        **kwargs
        ):
        super().__init__(**kwargs)
        self.is_expanded = expanded

    def extend_data(self, initial_ctx, menu, bound_handler, valid, trail=[]):
        super().extend_data(initial_ctx, menu, valid, bound_handler, trail)
        initial_ctx.update({
        'expanded' : (self.is_expanded or (menu.expand_trail and bound_handler in trail)),
        })  


    def get_wrap_css_classes(self, finished_data):
        classes = super().get_wrap_css_classes(finished_data)
        #print('submenu expanded' + str(finished_data))
        classes.add('submenu')
        if (finished_data['expanded']):
            classes.add('expanded')
        return classes

        
        


        
