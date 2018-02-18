from django.core.exceptions import ImproperlyConfigured
import os



#NB: decided against named tuples because of defaults. R.C.
class MenuItem:
    pass


class Separator(MenuItem):
    pass
 
     
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

    def __repr__(self):
        return '<{} name={}, url={} submenu={}>'.format(
            self.__class__.__name__,
            self.name,
            self.url,
            self.submenu,
        )   
  
#! need to normalise reverses, external urls, etc?
#? can reverses simply be reverse('news-year-archive', args=(year,))?
class URL(URLMenuItem):
    
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


#? test title field etc. exist
#? or provide auto defaults?
class QuerySet():
    '''
    If no information is given, an attempt is made to construct URLs 
    from Model data. There is no guarantee this will work, though-to 
    make sure, define.

    @param queryset can be any iterable of queries (including a dict)
    @param title_field to query for the title.
    @param url_field to query for url ids. This is fed to the template.
    @param url_template a template used to form urls/hrefs.
    @param use_absolute_url override the url creation attributes and try
    on the model to find an absolute url.
    @param icon_ref 
    '''
    queryset = None
    title_field = None
    url_field = 'pk'
    url_template = None
    use_absolute_url = False
    icon_ref=None
    #localize=False, 
    expanded=False 
    disabled=False
    validators=None
    attrs={}
        
    def __init__(self, queryset, 
        title_field=None, 
        url_field=None,
        url_template=None,
        use_absolute_url=False,
        icon_ref=None, 
        #localize=False, 
        expanded=False, 
        disabled=False,
        validators=None,
        attrs={}
    ):
        if (queryset):
            self.queryset = queryset  
        if (not self.queryset):
            raise ImproperlyConfigured("'queryset' attribute required")
        self.model = self.queryset.model
        fieldnames = [f.name for f in self.model._meta.fields]
        
        if (title_field):
            self.title_field = title_field
        if (not self.title_field in fieldnames):
          raise ImproperlyConfigured('title field requested but not in queryset model: model name:"{}" : title field:"{}"'.format(
          self.model._meta.object_name,
          title_field
          ))

        if (url_field):
            self.url_field = url_field
        if ((self.url_field) and (self.url_field != 'pk') and (not self.url_field in fieldnames)):
          raise ImproperlyConfigured('url field requested but not in queryset model: model name:"{}" : url field:"{}"'.format(
          self.model._meta.object_name,
          self.url_field
          ))
        
        if (url_template):
            self.url_template = url_template
        else:
            self.url_template = '{}{}{}{}{}{{}}'.format(
              os.sep,
              self.model._meta.app_label,
              os.sep,
              self.model._meta.model_name,
              os.sep,
              )
        
        #if ((self.url_field) and (not self.url_template)):
          #raise ImproperlyConfigured('If a url field is declared it must be given a template: model name:"{}" : url field:"{}"'.format(
          #self.model._meta.object_name,
          #self.url_field
          #))
                  
        if (use_absolute_url):
            self.use_absolute_url = use_absolute_url
        #if (not(url_field or self.use_absolute_url)):
            #raise ImproperlyConfigured("'url_field' or 'use_absolute_url' attribute required")
        if (icon_ref):
            self.icon_ref=icon_ref 
        #if (localize):
        #    self.localize=localize 
        if (expanded):
            self.expanded=expanded
        if (disabled):
            self.disabled=disabled
        if (validators):
            self.validators=validators
        self.attrs.update(attrs)
        
    def as_menu(self):
        menu = []
        for o in self.queryset:
            name = getattr(o, self.title_field)
            url = None
            if (self.use_absolute_url):
              url = o.get_absolute_url()
            else: 
              url = self.url_template.format(getattr(o, self.url_field).lower())
            icon_ref = self.icon_ref
            if (callable(self.icon_ref)):
              icon_ref = icon_ref()
            item = URL(name, url,
                icon_ref=self.icon_ref, 
                validators=self.validators,
                #localize=self.localize, 
                expanded=self.expanded,
                disabled=self.disabled,
                #attrs=self.attrs
                )
            menu.append(item)
        return menu

    #@property
    #def media(self):
    #    """Return all media required to render the widgets on this form."""
    #    return self.media


# May also have
# JavascriptAction?
