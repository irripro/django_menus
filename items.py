from django.core.exceptions import ImproperlyConfigured
from django.forms.widgets import Media

#! must do all the URL/attr gear of URL
class SubMenu():
    submenu = None
    
    def __init__(self, name, url, menu_ref,
            icon_ref=None, 
            icon_submenu_ref=None,
        ):
        self.menu_ref = menu_ref
        self.name = name
        self.url = url
        self.icon_ref = icon_ref
        self.icon_submenu_ref = icon_submenu_ref

class Separator:
    pass

  
  
#! need to normalise reverses, external urls, etc?
#? can reverses simply be reverse('news-year-archive', args=(year,))?
class URL():
    validators = []
    valid = False
    attrs={}
    media = Media()
    clean_url = None
    
    def __init__(self, name, url,
        icon_ref=None, 
        localize=False, 
        disabled=False,
        validators=[],
        attrs={}
        ):
        self.name = name
        self.url = url
        self.icon_ref = icon_ref
        self.localize = localize
        self.disabled = disabled
        if (validators):
            #! chain, if we stick with lists
            self.validators = validators
        self.attrs.update(attrs)
        
    def prepare_url(self, url):
        return url
        
    def run_validators(self, url):
        validated = True
        for v in self.validators:
            try:
                v(url)
            except ValidationError as e:
                validated = False
        return validated

    def clean(self):
        url = self.prepare_url(self.url)
        self.valid = self.run_validators(url)
        self.clean_url = url



        
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
