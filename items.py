import re
from django.core.exceptions import ImproperlyConfigured
from django.forms.widgets import Media


from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.utils.html import conditional_escape, html_safe, format_html
from collections import namedtuple

#! need a distinction beteween data given as options
#! ans later calculated (e.g. auto expanding)
#? use auto-attributed kwargs
#Person = collections.namedtuple('Person', 'name age gender')
#bob = Person(name='Bob', age=30, gender='male')
class MenuItem:
    str_tmpl = None
    wrap_css_classes = ''
    selected = False
    disabled = False

    def __init__(self, disabled=False):
        if (disabled):
            self.disabled = disabled


class Separator(MenuItem):
    str_tmpl = '<hr/>'
 
     
class URLMenuItem(MenuItem):
    def __init__(self, name, url, 
        validators=[],
        expanded=False, 
        disabled=False
        ):
        self.name = name
        self.url = url
        self.validators = validators
        self.expanded = expanded
        super().__init__(disabled=disabled)


     
                    
#! must do all the URL/attr gear of URL
class SubMenu(URLMenuItem):
    str_tmpl = '<a href="{url}">{icon}{name}</a>'
    submenu = None
    
    def __init__(self, name, url, menu_ref,
            icon_ref=None,
            validators=[], 
            expanded=False, 
            disabled=False,
        ):
        self.menu_ref = menu_ref
        self.icon_ref = icon_ref
        super().__init__(name, url, validators, expanded, disabled)

  
  
#! need to normalise reverses, external urls, etc?
#? can reverses simply be reverse('news-year-archive', args=(year,))?
class URL(URLMenuItem):
    str_tmpl = '<a href="{url}">{icon}{name}</a>'
    
    def __init__(self, name, url,
        icon_ref=None, 
        validators=[],
        expanded=False, 
        disabled=False,
        ):
        self.icon_ref = icon_ref
        super().__init__(name, url, validators, expanded, disabled)
        


        
class QuerySet():
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
