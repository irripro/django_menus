import warnings

#from django.forms.utils import flatatt, pretty_name
#from django.forms.views import Textarea, TextInput
from django.utils.functional import cached_property
from django.utils.html import conditional_escape, format_html, html_safe
from django.utils.inspect import func_accepts_kwargs, func_supports_parameter
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

__all__ = ('BoundHandler',)


#? menu parameter useless?
#? may take attributes? or classes?
@html_safe
class BoundHandler:
    "A Handler with a view instance and data"
    def __init__(self, handler, item_data):
        self.handler = handler
        self.item_data = item_data
        self._is_valid = True
        # used to contruct a tree of BoundHandlers, representing
        # the original item structure
        self.submenu = []
        
    def __str__(self):
        """Render this handler as an HTML view."""
        return self.as_view()

    def __repr__(self):
        return '<{} item={} valid={} wrap={}>'.format(
            self.__class__.__name__,
            self.item_data,
            self.is_valid,
            self.wrap
        )
        
    def __bool__(self):
        # BoundHandler evaluates to True.
        return True

    def as_view(self, view=None, attrs={}):
        """
        Render the handler by rendering the passed view, adding any HTML
        attributes passed as attrs. If a view isn't specified, use the
        handler's default view.
        """
        if not view:
            view = self.handler.view
            
        # add handler view-attrs and views attr. Both the below will
        # copy info over, protecting originals
        attrs.update(self.handler.get_view_attrs(view))
        attrs.update(view.attrs)
        
        #kwargs = {}
        #if func_supports_parameter(view.render, 'renderer') or func_accepts_kwargs(view.render):
        #    kwargs['renderer'] = self.form.renderer

        return view.render(request=None, attrs=attrs, **self.item_data.__dict__)

   #@property
    #def data(self):
        """
        Return the data for this BoundField, or None if it wasn't given.
        """
        #return self.handler.view.value_from_datadict(self.form.data, self.form.files, self.html_name)

    def values(self):
        """
        Return the value for this BoundField, using the initial value if
        the form is not bound or the data otherwise.
        """
        data = self.initial
        if self.menu.is_bound:
            data = self.handler.bound_data(self.data, data)
        return self.handler.prepare_data(data)

    def get_wrap_css_classes(self):
        """
        Return a string of space-separated CSS classes for the item wrap.
        """
        classes = self.handler.get_wrap_css_classes()
        print('classes:')
        print(str(classes))
        if (self.handler.view.is_disabled):
            classes.add('disabled')
        return classes

    def set_handler_attr(self, name, v):
        setattr(self.handler, name, v)
    
    @property
    def wrap(self):
        """
        True if this BoundHandler's view should be wrapped.
        """
        return self.handler.view.wrap

    @property
    def is_valid(self):
        """
        Did the BoundHandler pass validity. 
        Setting the property will take action for changing the 
        view. Depending on the attribute 'disable_invalid_items'
        (see Menu), the view may be disabled or hidden.
        """
        return self._is_valid 
        
    @is_valid.setter
    def is_valid(self, v):
        # tell the view if it is disabled.
        # (if item is hidden, the view is not used at all)
        self.handler.view.is_disabled = (not v)
        self._is_valid = v
        

                
      #@cached_property
    #def initial(self):
        #data = self.form.get_initial_for_handler(self.handler, self.name)
        #return data

    def validate(self, containing_menu_is_valid):
        '''
        Prepares the item data, validates, and informs the view of the 
        result.
        @return if processing is ok or not
        '''
        validated = True
        try:
            self.item_data = self.handler.clean(self.item_data)
        except ValidationError as e:
            validated = False
        self.is_valid = (containing_menu_is_valid and validated)
        return validated
        
    def get_view_attrs(self):
        '''
        Attribute dict to be used on every item of this type.
        '''
        #if not view:
        #    view = self.handler.view
        attrs = {}
          
        return attrs

    def get_view_css_classes(self):
        classes = super().get_view_css_classes()
        if (self.handler.view.is_expanded):
            classes.add('disabled')
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
