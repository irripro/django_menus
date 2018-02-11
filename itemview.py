import re
from django.core.exceptions import ImproperlyConfigured
from django.forms.widgets import Media
from django.template.loader import render_to_string

from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.utils.html import conditional_escape, html_safe, format_html



def rend_attrs(attrs):
    b = []         
    for k,v in attrs.items():
        if (v):
            #? What gets strings, what not?
            b.append(format_html('{0}="{1}"', k, v))
    return mark_safe(' '.join(b))



#! need a distinction beteween data given as options
#! and later calculated (e.g. auto expanding)
#? use auto-attributed kwargs
class ItemView:
    '''
    Encapsulate the rendering of a menu item.
    Some similarity to Django form.Widget.
    The only attributes on this and subclasses are user-definable options.
    
    @param str_tmpl a string formatter for the rendering. Inserted 
    elements should be named, nt positioned.
    @param wrap should this menu item be wrapped. Nearly always true, 
    but not always (e.g. separaters)
    '''
    str_tmpl = None
    '''
    Should this item be wrapped (in LI or DIV) by Menu
    '''
    wrap = True
    # internal
    #is_disabled = False
        
    # @param attrs attribute dict to add to the view. The data comes 
    # from this class; and from the handler, via boundhandler as_view() 
    def __init__(self, attrs=None):
        #? no need to copy now boundhander does the job
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}
            
    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.attrs = self.attrs.copy()
        memo[id(self)] = obj
        return obj

    def format_values(self, context):
        """
        Return context values as they should appear when rendered in a template.
        """
        pass
        
    def get_context(self, request, attrs, **kwargs):
        '''
        @param kwargs this the data from a menu item, as transformed by 
        a handler. It is all passed, as is, to the template context.
        '''
        context = {'view' : kwargs}
        context['view'].update({
            #'name': name,
            #'value': self.format_value(value),
            #'disabled' : self.is_disabled,
            'request': request,
            #'attrs': self.build_attrs(attrs),
            'attrs': attrs,
        })
        return context

    def append_css_class(self, context, class_name):
        '''
        Place extra classes into a view render. 
        '''
        ctx_view = context['view']
        if ('class' in ctx_view and ctx_view['class']):
            ctx_view['class'] = ctx_view['class'] + ' ' + class_name
        else:
            ctx_view['class'] = class_name
        return context

    def template_render(self, context):
        #! add exception - required
        pass
        
    def render(self, request=None, attrs=None, **kwargs):
        """
        Render the view as an HTML string.
        """
        ctx = self.get_context(request, attrs, **kwargs)
        #self.extend_css_classes(ctx)
        self.format_values(ctx)
        #print('ctx:' + str(ctx))
        return mark_safe(self.template_render(ctx))

    #- skip this, do it in boundfield
    #def build_attrs(self, extra_attrs=None):
        #"""Build an attribute dictionary."""
        #attrs = self.attrs.copy()
        #if extra_attrs is not None:
            #attrs.update(extra_attrs)
        #return attrs
        
    #something about datadisct....
        

        
class URLView(ItemView):
    # NB: URL is regarded as an attr so it can be eliminated entirely.
    # In the rest of the item processing chain, it is a separate item.
    # It is only concaternated right at the end, in the string 
    # template format.
    str_tmpl = '<a {attrs}>{icon}{name}</a>'
    is_expanded = False

    def __init__(self,
        attrs = None
        ):
        super().__init__()
    
    def _rend_icon(self, icon_ref):
        icon = mark_safe('<svg class="menu-item-icon" xmlns="http://www.w3.org/2000/svg" width="0" height="0" viewBox="0 0 0 0" ></svg>')
        if (icon_ref is not None):
            icon = format_html('<img class="menu-item-icon" src="{}" />',
            icon_ref
            )
        return icon

    def get_context(self, request, attrs, **kwargs):
        context = super().get_context(request, attrs, **kwargs)
        # do we want to expand here?
        
        ctx = context['view']
        # if disabled, remove href
        if (ctx['disabled']):
            ctx['url'] = ''
        return context

    #! where are attrs from?
    def template_render(self, context):
        ctx_view = context['view']
        if (ctx_view['url']):
            ctx_view['attrs']['href'] = ctx_view['url']
        return format_html(self.str_tmpl,
            attrs = rend_attrs(ctx_view['attrs']),
            icon = self._rend_icon(ctx_view['icon_ref']),
            name = ctx_view['name']
            )



class SeparatorView(ItemView):
    str_tmpl = '<hr{attrs}/>'
    wrap = False
    
    #! where are attrs from?
    def template_render(self, context):
        return format_html(self.str_tmpl,
            attrs = rend_attrs(context['view']['attrs']),
            )



class QuerySetView():
    queryset = None
    title_field = None
    url_template = None
    use_absolute_url = False
    icon_ref=None, 
    localize=False, 
    disabled=False,
    validators=None,
    attrs={}
        
    def __init__(self, queryset, title_field=None, url_field=None, use_absolute_url=False,
        icon_ref=None, 
        localize=False, 
        disabled=False,
        validators=None,
        attrs={}
    ):
        if (queryset):
            self.queryset = queryset  
        if (not self.queryset):
            raise ImproperlyConfigured("'queryset' attribute required")
        if (url_field):
            self.url_field = url_field
        if (use_absolute_url):
            self.use_absolute_url = use_absolute_url
        if (not(self.url_field or self.use_absolute_url)):
            raise ImproperlyConfigured("'url_field' or 'use_absolute_url' attribute required")
        if (icon_ref):
            self.icon_ref=icon_ref 
        if (localize):
            self.localize=localize 
        if (disabled):
            self.disabled=disabled
        if (validators):
            self.validators=validators
        self.attrs.update(attrs)
        
    def get_menu(self, url):
        menu = []
        for o in self.queryset:
            name = o.title_field
            url = o.get_absolute_url() if (self.use_absolute_url) else o.title_field
            item = URL(name, url,
                icon_ref=self.icon_ref, 
                localize=self.localize, 
                disabled=self.disabled,
                validators=self.validators,
                attrs=self.attrs
                )
            menu.append(item)
        return menu

    @property
    def media(self):
        """Return all media required to render the widgets on this form."""
        return self.media


# May also have
# JavascriptAction?
