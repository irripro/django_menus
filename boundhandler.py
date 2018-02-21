import warnings

#from django.forms.utils import flatatt, pretty_name
#from django.forms.views import Textarea, TextInput
from django.utils.functional import cached_property
from django.utils.html import conditional_escape, format_html, html_safe
from django.utils.inspect import func_accepts_kwargs, func_supports_parameter
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

__all__ = ('BoundHandler',)


#? menu parameter useless?
#? may take attributes? or classes?
#@html_safe
class BoundHandler:
    '''
    Bind a handler with a view instance and accept data.
    One is constructed for every menu item. Cached across web calls.
    
    '''
    #! need to get rid of menu, it is mutable, and bound handler is cached.
    #! or pass menu opts.
    def __init__(self, menu, handler, item_data):
        self.menu = menu
        self.handler = handler
        self.item_data = item_data
        # used to contruct a tree of BoundHandlers, representing
        # the original item structure
        self.submenu = []
        
    #def __str__(self):
        """Render this handler as an HTML view."""
        #return self.as_view()

    def __repr__(self):
        return '<{} item={} wrap={}>'.format(
            self.__class__.__name__,
            self.item_data,
            #self.is_valid,
            self.wrap
        )
        
    def __bool__(self):
        # BoundHandler evaluates to True.
        return True

    def get_initial_context(self, valid, trail):
       '''
       Get the configuration data as a context.
       The config data is extended with handler-configured data. This 
       data may be informed by other data such as validity results.
       
       @return a dict version of the data. 
       '''
       ctx = self.item_data.__dict__.copy()
       self.handler.extend_data(ctx, self.menu, self, valid, trail)
       return ctx
       
    def as_view(self, initial_context, view=None, attrs={}):
        """
        Render the handler by rendering the passed view, adding any HTML
        attributes passed as attrs. If a view isn't specified, use the
        handler's default view.
        """
        if not view:
            view = self.handler.view
            
        # add handler view-attrs and views attr. The below will
        # copy info over, protecting the originals
        #? could be cached? Or init?
        #! use extend logic, not this
        attrs = attrs.copy()
        attrs.update(self.handler.get_view_attrs(view))
        attrs.update(view.attrs)
        return view.render(request=None, attrs=attrs, **initial_context)
        
        
    def get_wrap_css_classes(self, finished_data):
        """
        Return a string of space-separated CSS classes for the item wrap.
        """
        classes = self.handler.get_wrap_css_classes(finished_data)
        return classes


    @property
    def wrap(self):
        """
        True if this BoundHandler's view should be wrapped.
        """
        return self.handler.view.wrap
    
    def validate(self, request, containing_menu_is_valid):
        '''
        Prepares the item data, validates, and informs the view of the 
        result.
        @return if processing is ok or not
        '''
        validated = containing_menu_is_valid
        try:
            for validator in self.item_data.validators:
                validator(request, self.item_data)
            self.handler.validate(request, self.item_data)
        except ValidationError as e:
            validated = False
        return validated

    def get_view_attrs(self):
        '''
        Attribute dict to be used on every item of this type.
        '''
        return {}

    def get_view_css_classes(self):
        classes = super().get_view_css_classes()
        return classes

       
#@html_safe
#class BoundWidget:
    #"""
    #A container class used for iterating over views. This is useful for
    #views that have choices. For example, the following can be used in a
    #template:

    #{% for radio in myform.beatles %}
      #<label for="{{ radio.id_for_label }}">
        #{{ radio.choice_label }}
        #<span class="radio">{{ radio.tag }}</span>
      #</label>
    #{% endfor %}
    #"""
    #def __init__(self, parent_view, data, renderer):
        #self.parent_view = parent_view
        #self.data = data
        #self.renderer = renderer

    #def __str__(self):
        #return self.tag(wrap_label=True)

    #def tag(self, wrap_label=False):
        #context = {'view': self.data, 'wrap_label': wrap_label}
        #return self.parent_view._render(self.template_name, context, self.renderer)

    #@property
    #def template_name(self):
        #if 'template_name' in self.data:
            #return self.data['template_name']
        #return self.parent_view.template_name

    #@property
    #def id_for_label(self):
        #return 'id_%s_%s' % (self.data['name'], self.data['index'])

    #@property
    #def choice_label(self):
        #return self.data['label']
