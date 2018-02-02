import re
import itertools

from django.core.exceptions import ImproperlyConfigured
from django.forms.widgets import Media


from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.utils.html import conditional_escape, html_safe, format_html

from .itemview import ItemView, SeparatorView, URLView
from .boundhandler import BoundHandler




#! need a distinction beteween data given as options
#! ans later calculated (e.g. auto expanding)
#? use auto-attributed kwargs
#? make a queryset version
#? include validators from items?
class ItemHandler:
    '''
    Prepare and validate items.
    Can be subclassed to handle data input from specific items. 
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
            
        # Hook into self.widget_attrs() for any Field-specific HTML attributes.
        extra_attrs = self.view_attrs(view)
        if extra_attrs:
            view.attrs.update(extra_attrs)
            
        self.view = view or self.view

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
        return item

    def clean(self, item):
        '''
        @return clean data
        @throw validation error
        '''
        item = self.prepare_item(item)
        return self.run_validators(item)

    #-
    def view_attrs(self, view):
        """
        Given a View instance (*not* a View class), return a dictionary of
        any HTML attributes that should be added to the View, based on this
        Handler.
        """
        return {}
        

        
        
class URLHandler(ItemHandler):      
    view = URLView
       
    def __init__(self, 
        view=None,
        validators=(),
        expanded=False,
        disabled=False
        ):
        view.is_expanded = expanded
        view.is_disabled = disabled
        super().__init__(view=view, validators=validators)

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




#class SubMenuHandler(ItemHandler):                 
    #pass

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
        
        


        
