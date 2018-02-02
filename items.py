
#NB: decided against named tuples because of defaults. Later? R.C.
class MenuItem:
    str_tmpl = None



class Separator(MenuItem):
    str_tmpl = '<hr/>'

 
     
class URLMenuItem(MenuItem):
    def __init__(self, name, url, 
        validators=[],
        expanded=False, 
        ):
        self.name = name
        self.url = url
        self.validators = validators
        self.expanded = expanded
        super().__init__()

    def __repr__(self):
        return '<{} name={}, url={}>'.format(
            self.__class__.__name__,
            self.name,
            self.url,
        ) 

                         
class SubMenu(URLMenuItem):
    str_tmpl = '<a href="{url}">{icon}{name}</a>'
    submenu = None
    
    def __init__(self, name, url, menu_ref,
        icon_ref=None,
        validators=[], 
        expanded=False, 
        ):
        self.menu_ref = menu_ref
        self.icon_ref = icon_ref
        super().__init__(
            name,
            url,
            validators, 
            expanded
        )

  
  
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
        super().__init__(
            name,
            url,
            validators, 
            expanded
        )        


        
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
