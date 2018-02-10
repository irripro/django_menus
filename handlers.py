import re
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
class ItemHandler:
    '''
    Configuration and validation of item data.
    For eachtype of menu item, there is a handler. The handler contains
    configuration which is overall for the item. The configuration can 
    be set by the user.
    Handlers are constructed per menu, then cached across web calls. Any
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
        #? Not sure about this. Let boundhandler, which also has 
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
        If the data is normalised or some other mutaation, then it must 
        be copied.
        '''
        return item
        
    def run_validators(self, item):
        validated = True
        for v in self.validators:
            #try:
                v(item)
            #except ValidationError as e:
            #    validated = False

    def clean(self, item):
        '''
        @return clean data
        @throw validation error
        '''
        item = self.prepare_item(item)
        self.run_validators(item)

    def get_view_attrs(self, view):
        """
        Given a View instance (*not* a View class), return a dictionary of
        any HTML attributes that should be added to the View, based on this
        Handler.
        """
        return {}
        
    def get_wrap_css_classes(self, finished_data):
        return set()
        
    def get_extension_data(self, valid,  bound_handler, trail=[]):
        '''
        Add data to extend the config data.
        When this data is requested, the configuration data is validated 
        and transformed into an initial_context.
        
        Unlike the handler data, which is cached and
        immutable, the extended data can be modified by other code in 
        Boundhandler, Menu, etc. The values in the dict act as a 
        default. However, this method recieves some useful data,
        including the bound handler which called it. This data may be 
        enough to make useful settings to extended data.
        
        @return  dict of data to update the initial context.
        '''
        return {}
        
        
        
        
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
        
    def get_extension_data(self, valid, bound_handler, trail=[]):
        d = super(). get_extension_data(valid, trail)
        d.update({
        'selected': (bound_handler in trail),
        'disabled':  (not valid),
        })
        return d

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

    def get_extension_data(self, valid,  bound_handler, trail=[]):
        d = super().get_extension_data(valid, trail)
        d.update({
        'expanded' : self.is_expanded or (bound_handler in trail),
        })        
        return d

    def get_wrap_css_classes(self, finished_data):
        classes = super().get_wrap_css_classes(finished_data)
        #print('self.is_expanded' + str(self.is_expanded))
        classes.add('submenu')
        if (self.is_expanded or finished_data['expanded']):
            classes.add('expanded')
        return classes

####
    ##! Get selectors going
    ##! what is path absolute?
    ##! match whole or part?
    ##? What this does is, finally, add a CSS class
    #def match_url(self, path):
        #"""
        #match url determines if this is selected
        #"""
        ##if request.user.is_authenticated:
        #print('slct path:')
        #print(str(path))
        #matched = False
        #if (not self.clean_url):
             #raise ImproperlyConfigured('match_url requested before validation')
        ##if self.exact_url:
        ##    if re.match("%s$" % (self.url,), request.path):
        ##        matched = True
        ##elif re.match("%s" % self.url, request.path):
        
        ##! not good enough. 
        ## What about slashes? hash ends?
        #if re.match("%s" % self.clean_url, path):
            #matched = True
        #return matched
        
        


        
