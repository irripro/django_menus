
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, html_safe, format_html



#from django.conf import settings
#from .utils import get_menu_from_apps
#from . import defaults

#from django.core.exceptions import ImproperlyConfigured





#MenuSet    
#! rename menurenderer
class MenuRenderer2():
   pass
        
class MenuRenderer:
    entries = {}
    template = None
    attrs = {}
    _built_attrs = ''
    _css_classes = ''
    
    def __init__(self, entries, attrs={}):
        self.entries = entries
        css_classes = attrs.pop('class', None)
        if (css_classes):
          self._css_classes = ' '.join(css_classes)
        if (not attrs):
            attrs = self.attrs
        self._built_attrs =  self._build_attrs(attrs)


    
    def _build_attrs(self, attrs):
        b = []         
        for k,v in attrs.items():
            b.append('{0}="{1}"'.format(k, v))
        return ' '.join(b)
        
    #! test 'active'
    def _html_output(self, row_tmpl):
        "Output HTML. Used by as_table(), as_ul(), as_p()."
        b = []
        for e in self.entries:
             print('rend:')
             print(str(e))
             attrs = self._built_attrs
             css_classes = 'class="{}{}"'.format(
                 self._css_classes,
                 ' active' if (e['selected']) else ''
             )
             entry_str = format_html(row_tmpl,
                 attrs= attrs,
                 icon= e['icon_class'],
                 url= e['url'],
                 name= e['name']
             )             
             b.append(entry_str)

        return mark_safe('\n'.join(b))

    def as_ul(self):
        "Return this menu rendered as HTML <li>s -- excluding the <ul></ul>."
        return self._html_output(
            row_tmpl='<li {attrs}>{icon}<a href="{url}">{name}</a></li>',
            )

    def as_div(self):
        "Return this menu rendered as HTML <div>s -- excluding a wrapping <div></div>."
        return self._html_output(
            row_tmpl='<div {attrs}>{icon}<a href="{url}">{name}</a></div>',
            )
            
    def __str__(self):
        return self.as_ul()

    def __repr__(self):
        return '<%(cls)>' % {
            'cls': self.__class__.__name__,
            #'valid': is_valid,
            #'fields': ';'.join(self.fields),
        }
