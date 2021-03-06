Django Menus
============
A menu generator for Django applications.

Uses a hard coded base. As the author of another Django app wrote, "Who wants to use Admin to maintain menus?" (a few other applications use this approach).

By default, the app renders menu data as CSS-only hover-action dropdown menus. There are also files/support for creating one-click JavaScript menus. The HTML output is data with no action enabled, so can be used to enable whatever style and action of menu you want.

When to use
------------
This is a sophisticated menu builder. It has an API with similarities to django.Form. Why use a powerful (probably hungry?) app like this? For a simple menu you should not. In Django, write links into a template.

The time to use this app is when you want long-term maintainability. To be able to come back after a year and know how to make substancial changes. Or when you have a deep menu system and your templates are becoming cluttered.

There are minor reasons also. If you are looking for fancy menus, but are not using a front-end bundle like Bootstrap, this app has front-end theming. Some of the themes are close to responsive displays; you only need to design/specify a container.  

The app also provides some actions that would be difficult otherwise. You may have a small menu, but if you would like to auto-expand to the current page, this app can do that.


Alternatives
------------

Category apps
~~~~~~~~~~~~~
The word 'category' unfortunately covers several data structures. There is a big difference between categories that are simple 'groups' (the casual meaning) and in a 'tree' (taxonomy, what people sometimes mean, is used in libraries, etc.). Trees, especially, can be implemented and presented in several ways.

Menu structure is a taxonomy structure. So catgory/taxonomy apps can be used for menu-building. But they may be short of conveniences/DRY simplicities.

django-catalog
    https://pypi.python.org/pypi/django-catalog/2.1.1
    Unused? Tree structures. Admin interface(!)
 
redsolutioncms.django-catalog 2.0.
    https://pypi.python.org/pypi/redsolutioncms.django-catalog/2.0.2
    Earlier version of above.

django-catalogue 0.1dev
    https://pypi.python.org/pypi/django-catalogue/0.1dev
    Abandoned? Raw looking app with little code.

django-categories 
    https://djangopackages.org/packages/p/django-categories/ 
    Much used app. Tree structures.

django-category
    https://github.com/praekelt/django-category
    Seperate table. In-use system for categorising and tagging models. 


Menu systems
+++++++++++++
A menu system is, effectively, a taxonomy or grouping structure with links as data. It will, to do this, have helpers or automation.

Possible features: templating of entries, injection of Django features like reverse(), reoredering of entries, provision for internal/external links, parent and sibling delivery, breadcrumb (path) delivery, permission handling (not always important in Django, fundamentally handled on views), auto generation of links (and does that stash/cache?), select current item, GUI.

Once we start on menus, possibilities escalate. Stars for the two most-used packages in django-papckages.

django-garpix-menu 0.1.0
    https://pypi.python.org/pypi/django-garpix-menu/0.1.0
    Marked alpha and maybe dead.

django-menu-generator 1.0.2
    https://pypi.python.org/pypi/django-menu-generator/1.0.2
    Non-db menu builder. Cute.

django-simple-menu2 2.0.7 *
    https://pypi.python.org/pypi/django-simple-menu2/2.0.7
    https://github.com/borgstrom/django-simple-menu
    Handbuilt simplicity. And we seem to have major forks. Much used.

django-treemenus2 0.9.3
    https://pypi.python.org/pypi/django-treemenus2/0.9.3
    Well, many of the others are tree too. Sibling/parent handling etc.

django-navbar 0.3.0
    https://pypi.python.org/pypi/django-navbar/0.3.0
    Dead. Promises breadcrumbs

django-object-links 0.1.6-alpha-1
    https://bitbucket.org/xenofox/django-object-links/
    fork of dead http://code.google.com/p/django-links/.

django-surfing 0.0.1
    dead. Big promises.

django-treemenu 0.1.1
    https://pypi.python.org/pypi/django-treemenu/0.1.1
    Dead. More promises. Much used, though, many forks.

django-navigen 0.1.3
    https://pypi.python.org/pypi/django-navigen/0.1.3
    Genuinely different; dynamically rebuilds trees by permissions.

django-menu 0.1.11 *
    https://pypi.python.org/pypi/django-menu/0.1.11
    Simple, probably well-considered app. Only seems to have two levels. Much used.

django-sitemenu 0.0.4
    https://pypi.python.org/pypi/django-sitemenu/0.0.4
    Another well-considered app. GUI.

redsolutioncms.django-menu-proxy 0.1.2
    https://pypi.python.org/pypi/redsolutioncms.django-menu-proxy/0.1.2
    Dead project. Dynamic menu.


Source description
------------------
Unlike much of my Django code, this app originated in other code, a Django application named 'menu-generator'. I do not have the technical knowhow nor computing capability to fork the project, so started again. The app is now nothing like the elegance of 'menu-generator'. It was rewritten to gather much of the API from Django Forms. So, the Menu class is like the Django class 'Form'. Menu is populated with ItemHandlers (like Fields) which contain ItemViews (like Widgets).

However, while this will help explain the overall structure, be careful of comparing too closely. Menu is much simpler than Form. The app refines the purpose of ItemHandlers, so they are not like Fields and have important extra abilities. Probably best to say, knowing this app is like Django Forms means you may be able to guess what kind of features it offers, and how to use them (you can make custom menu items. You can add attributes to menu items of one type etc.).  

https://pypi.python.org/pypi/django-menu-generator/1.0.2
https://github.com/un33k/django-menuware

Some hints are taken from the Drupal module NiceMenus_. And the old Drupal router.


Current state
-------------
As it arrives. No guarentees. But working.


Installation
------------
Place the app in a Django environment. In settings.py, ::

    INSTALLED_APPS = [
        ...
        'django_menus',
    ]

Done (there are various minor reasons why this app likes to be declared).


Note on the HTML output
-----------------------

Like the Django Form class, Menu output has no surrounding div, ul, or table tags. These need adding, something like this, ::

    {% load menu_generator %}

    {% get_menu "site/NAV_MENU_LEFT" as site_menu %}
    <ul>
      {{ site_menu }}
    </ul>
        
        
Quickstart
----------
Build a menu configuration in an app. Put it in a file 'menubase.py'. The menu is a dict containing classes, and the dict name must be 'MENUS'. Here's an example, ::
    
    from django_menus import SubMenu, URL, Separator
    
    MENUS = {
        'NAV_MENU_SITE_DEPARTMENTS': [
            URL("Classics", "/classics/"),
            URL("Sociology", "/sociology/"),
            URL("Fine Art", "/fineart/"),
        ]
        'NAV_MENU_SITE_WORK_WITH_US': [
            URL("Help", "/help/"),
            URL("By department", "/department/conferences/"),
            URL("Conferences", "/conferences/"),
            Separator(),
            URL("Contact", "/contact/"),
        ],    
        'NAV_MENU_SITE_RESOURCES': [
            URL("Map", "/map/"),
            URL("Plant", "/plant"),
            URL("Research", "/research"),
            URL("Events", "/conferences/"),
            URL("Projects", "/projects/"),
        ], 
        'NAV_MENU_SITE_ABOUT': [
            URL("Dates", "/dates/"),
            URL("Annual Report", "/report/annual/"),
            URL("Jobs", "/jobs/"),
        ],
        'NAV_MENU_SITE': [
            URL("Home", "/home/"),
            SubMenu("Departments", "#", 'NAV_MENU_SITE_DEPARTMENTS'),
            SubMenu("Work with us", "#", 'NAV_MENU_SITE_WORK_WITH_US'),
            SubMenu("Resources", "#", 'NAV_MENU_SITE_RESOURCES'),
            SubMenu("About", "#", 'NAV_MENU_SITE_ABOUT'),
            URL("Search", "/search/"),
        ]
    }
  
Put the menu into the template. Two ways, easiest way is using the template tag. The template tag can be in any template, not only the django_menu app (and the config can be anywhere too, as long as it has the right filename).

In the template, you need to load the tag code, then a couple of imports for base css and a theme, and then to place the menu-generating tag, ::

    {% load menu_generator %}

    <link href={% static 'django_menus/django_menu_base.css' %} type="text/css" media="all" rel="stylesheet">
    <link href={% static 'django_menus/django_menu_too_cool_to_be_hip.css' %} type="text/css" media="all" rel="stylesheet">

        # Note the menu name is a little URL: app_name + '/' + menu_name
        {% get_menu "site/NAV_MENU_SITE" as site_menu %}

        <ul class="dmenu dmenu-css dmenu-right dmenu-horizontal dm-toocool">
          {{ site_menu }}
        </ul>
        
Now go look at a page which uses the template.
        
        
Data Structure and usage
------------------------

Menu Construction using MenuItems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Menubase has a structure like above. You can find the MenuItem definitions in the file items.py.


Validation
++++++++++
MenuItems can be individually validated. Also, items of a type can be generally validated in an ItemHandler.

Like django.core validators, Django_menus validators work by throwing a ValidationError. But they do not have the same signature as django.core validators, ::

    def validation_func(request, item_data):
        """
        Returns True if request.user authenticated else returns False
        """
        if (validation fails):
            raise ValidationError(_('Not Valid.'), code='invalid')
        
Several validators have been built in to django_menus and can be found in django_menus.validators. These are mainly for authentification. Of course, blocking a menu item from showing is not a block on access. But it is user-friendly to show a user only what they can access.

The validators recieve menu item data. The menu item is in a raw state, a dict from the the configuration data (though there is a prepare() hook to do data conversion or normalization, if necessary). This data allows the validation to, for example, target specific types of URLS. Please bear in mind that menu item data may be untrusted (from the DB via. menuitems.QuerySet).

Validators are set (in MenuItems or in ItemHandlers) as a list of functions e.g. for a validator in a MenuItem, ::

    from django_menus import SubMenu, URL, Separator, QuerySet
    from django_menus import validators
    
        'NAV_SITE_MENU': [
            ...,
            URL("Admin", "/site/page/admin/", validators=[validators.is_authenticated]),
        ]
        
Validators are mainly run in the ItemHandlers, but you do not need to know much about the system.

    
Half-dynamic construction
+++++++++++++++++++++++++
One of the MenuItems is not a subclass of MenuItem, but is a Menutem generator. It is called QuerySet.

Queryset can construct menu items by querying the database. However, django_menus is an app that uses static, cached, data. So the results of a QuerySet injection are static and cached. The DB query is only made once, when the server boots. To make the query again, the server will need to be rebooted.
 
QuerySet is a very configurable class. It can be subcalssed to preset most of it's attributes, or set through the init parameters (like a Django View). Here is an example of QuerySet being used to recover a set of page objects, then transform them into MenuItems, ::

    'SITE_MENU_SPECIAL_PAGES': QuerySet(Page.objects.all(), title_field='title', 
    url_field='title', url_template="/site/page/{}").as_menu()

You can see from the input parameters that the QuerySet is probably constructing MenuItems (it is). If the model Page contains the kind of support pages that might be found in Django flatpages, the output may be like this, ::

            URL("Help", "/site/page/help"),
            URL("Contact", "/site/page/contact"),
            URL("About", "/site/page/about"),
            ...
            
one for every page in the model Page.
 
Queryset makes some efforts to guess input parameters. If not given a url_field, it defaults to using a 'pk' field. It can be asked to use Django Model absolute URLs. It has an attribute 'url_template', which is an overridable string template for URL/href construction. It accepts a hard-coded or callable parameter to construct 'icon_ref's.
 
Let's talk about what QuerySet can and can not do. You can not construct menus from free-flowing datasets. For example, QuerySet will not produce lists of users on a social media site, or a list of products for a shop. The server would need to be restarted when a new user or product was added (NB: I decided, somewhere in the middle of the construction, not to make a full-dynamic menu system. The DB hits would be multiple, despite Django ORM caching. And it would make the app a complex and hybrid codebase, for not much gain).

However, some data is not free-flowing. It is changed rarely, and you could justify a server restart for such data changes. I'm thinking now of fundamental changes to an administation interface, or a list of departments on a shopping site. Or, as in the example above, support pages for a small site. QuerySet can produce such lists, and produce them using a very DRY configuration (i.e. the above example is one line, for several menu entries, which are generated, on a restart, automatically). 

Incidentally, this is a mechanism used by other URL systems. Django's URL handling works like this, as does the router in the Drupal CMS. Though configuarable, they need restarts, so they can cache (though Drupal offers cache-expiry). Django_menus is not as extensive as those apps, but you can think of the app in the same way.


MenuManager
~~~~~~~~~~~~
You can use a MenuManager to recover menu data, ::

    MenuManager(self, app, menu_name)
    
There's not much more to say about that class. Menumanager is called automatically and internally by the Menu class.


Menu
~~~~~
Handles overall menu construction. Which means storage, validation, and rendering. Output can be as DIV or LI. Call str() and Menu will output with the default, LI, ::

    > Menu('SITE_MENU', app_name='site-app', expand_trail=True)

Menu also builds what are called 'URL trails'. Any menu item data which contains a 'url' attribute is checked, and the path noted in a dict of paths. Matching the end point of these trails against requests, Menu can guess if the current page is in the menu. If it is, menu can add classes to display that item in various ways.

This behaviour is not used often in desktop GUIs, but is popular in web GUIs. It has advantages, especially in long menus of content ('you (the user) are currently at page ...').



Options
+++++++
disable_invalid
    If true, and a menu item fails validation, it is not hidden (the 
    default) but 'greyed out' and hrefs removed (similar 
    to a desktop GUI showing non-applicable actions). 
expand_trail
    If True, and the current page can be found in the trails (however 
    deep it is nested), the menu is expanded to show that item.
select_trail
    If True, and the current page can be found in the trails (however 
    deep it is nested), the menu has CSS class 'select' on the trail items.
select_leaf
    If True, and the current page can be found in the trails (however 
    deep it is nested), the menu has CSS class 'select' on the target item.


Trail matching
++++++++++++++
If the configuration has URL items (likely), then Menu will build a trail
through the configuration to them.

Sometimes it is useful not to want an exact match. A user visits a shop,
the site builders provide a menu for the departments, the user would 
like to see the department selected. The user is at, ::

    /jewellery/bangles/plastic/43

The department menu contains only configuration for, ::

    URL("Jewellery", "/jewellery"),
    URL("Garden", "/garden"),
    URL("Lighting", "/lighting"),
    ...

You can define a different match_key function for the menu. A handful 
of key-defining functions are builtin. If the menu in the template (or any Menu) defines, ::

        {% get_menu "site/DEPARTMENT_MENU?trail_key=HEAD1;select_leaf=True" as site_menu %}

then HEAD1 strips the path, ::

    /jewellery/bangles/plastic/43

to, ::

    /jewellery
    
before a match is tried. Now it matches and the /jewellery item in the 
department menu will be selected.

TAIL match_key functions can also be used. These are useful for tab-type
menus.


Placement
~~~~~~~~~
The HTML can be placed in a template in two ways. You can use a view and place the output onto a context, then render in the template. This allows customization, because the Menu class allows several custom settings, and custom handling of how item data is rendered, ::

    def get_context():
        ...
        context.update({
            'menu': Menu('site menu', app_name='site-app', expand_trail=True)
        })
        return context
       
But most people will not need that. If you do not, you can output from the template using the template tag, ::

    {% load menu_generator %}

        ...
        
        # Note the menu name is a little URL: app_name + '/' + menu_name
        {% get_menu "site/NAV_MENU_SITE" as site_menu %}

        <ul class="dmenu dmenu-css dmenu-right dmenu-horizontal">
          {{ site_menu }}
        </ul>

Note the little path used to refer to the menu. Django_menu uses the app name to namespace menus. So you can have two 'SIDEBAR_MENU's in the same installation, if they are in different apps.

Not only that, but the little URL allows you to put init parameters into Menu. This is nowhere near the level of customisation available from using a context and subclassing, but useful, e.g. ::

    {% load menu_generator %}

        ...
        
        # Note the menu name is a little URL: app_name + '/' + menu_name
        {% get_menu "site/NAV_MENU_SITE?trail_key=TAIL;expanded=True;" as site_menu %}

        <ul class="dmenu dmenu-css dmenu-right dmenu-horizontal">
          {{ site_menu }}
        </ul>

Don't expect much of the URL parse code. If you are wondering, yes, the URL means the app can work round the one-parameter-only limitation of Django template filters. 
        
        
Action and Styling
~~~~~~~~~~~~~~~~~~ 
The output from Menu is HTML. From there you may wish to devise your own style. Or it may be that you want to modify the HTML to work with existing CSS (and JS?) from another source. That's ok, the section below is optional and entirely separate from the HTML generation.

But maybe you want a menu and have no framework you need to match. Or you want to style the menus to match a site. Django_menus comes with a full action/theming structure you can follow. Or get some inspiration and a start.

The basic action is a 'hover'-action CSS-only menu. There are options to turn the menus into 'click'-action using Javascript. You'll need to skip down to see how to do that. 


I should claim how fabulous this is, which it can be. However, I've not worked the code through. Some options and themes can give strange and marvelous results. But give it a go because, if it gets you part-way down the road, that's a start, right?



Default CSS, themes, and overriding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
WARNING
+++++++
The app includes little CSS files. They may be small, but they are advanced. Styling a CSS menu is not simple. For example, the menu needs space before item text. But most menus do not need space before top-level horizontal items (no icons there, usually). You can, to add space, set a width on the embedded icon IMG. To avoid the top level, you can select the horizontal menu, and kill spacing, or select only submenus to space, or go down a level e.g. .dm-desktop ul .menu-item-icon {width: 14px; margin: 0 2px;}.

Anchors often have browser styling, and need direct selection. If you want to customize a submenu mark, it's a background image, and you need a .png at least, which can be difficult to position without 'vertical-align'. If borders are added to items, the alignment will walk up and down, depending on the box-model. A theme that enables full support for django_menus will need to respond to 'selected' and 'expanded' classes, and have left/right/down variants.

You may work faster if you copy and modify. If you do not do this as a day job, it can take considerable time.


After warning
+++++++++++++
The menu tags, or a context injection, deliver a pre-rendered menu HTML. This, in a browser, looks promising (if you are a glass-half-full person) but is not finished product.

First, a template needs, ::

    {% load static %}

    <link href={% static 'django_menus/django_menu_base.css' %} type="text/css" media="all" rel="stylesheet">

Either via '{{ media }}' or, as above, a direct import.

django_menu_base.css delivers basic positioning and CSS action for a menu. Add these classes to the UL tags which wrap the menu, ::

        {% load menu_generator %}

        {% get_menu "site/SITE_MENU" as site_menu %}
        <ul class="dmenu dmenu-css dmenu-right dmenu-horizontal">
          {{ site_menu }}
        </ul>        
        
Any depth in the menu will disappear (which is correct, don't panic).

'dmenu' sets some known basics (e.g. "submenus do not initially show"). 'dmenu-css' sets CSS show-on-hover action. 'dmenu-right' opens submenus to the right ('dmenu-left' to the left). 'dmenu-horizontal' sets the first entries in the menu horizontal.

You can mix these CSS modules (though they can give wierd results). No directions gives a push-down menu stack, ::

        {% load menu_generator %}

        {% get_menu "site/SITE_MENU" as site_menu %}
        <ul class="dmenu dmenu-css">
          {{ site_menu }}
        </ul>  
        
Anyway, the menu looks tidier. More importantly, if you hover elements, you will find the menu operates as you asked. But it looks... basic. The menu may open in wild positions (these classes set no widths/heights/borders etc.).

You can add your own CSS, via Media or directly. Or you can have a look at the sample themes. Themes are in django_menu/static/... Add this to load the 'desktop' theme, ::

    <link href={% static 'django_menus/django_menu_desktop.css' %} type="text/css" media="all" rel="stylesheet">

Then add the theme class to the wrapping UL tags, ::

        {% load menu_generator %}

        {% get_menu "site/SITE_MENU" as site_menu %}
        <ul class="dmenu dmenu-css dmenu-right dmenu-horizontal dm-desktop">
          {{ site_menu }}
        </ul> 
        
So,


.. figure:: https://raw.githubusercontent.com/rcrowther/django_menus/master/docs/images/desktop_menu.png
    :width: 160 px
    :alt: menu screenshot
    :align: center
    
Not flashy.

Ok, let's try a push-down theme, ::
    
    <link href={% static 'django_menus/django_menu_machinery.css' %} type="text/css" media="all" rel="stylesheet">


    {% load menu_generator %}

    {% get_menu "site/SITE_MENU" as site_menu %}
    <ul class="dmenu dmenu-css dm-machinery">
      {{ site_menu }}
    </ul> 

So,

.. figure:: https://raw.githubusercontent.com/rcrowther/django_menus/master/docs/images/machinery_menu.png
    :width: 160 px
    :alt: menu screenshot
    :align: center
    
Maybe pushing it there, huh, son?


'click'-action Javascripted menus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There is also a Javascript solution (which uses the JQuery from Django admin). Javascript action offers a fundamentally different experience, as the menu will not work on hover, but on clicking. This may or may not be a preference. Click actions also influence design (hover themes will not work well for click themes, and visa-versa). Before you ask, yes, I know CSS can do click menus, and that JS can do hover menus. I decided against both paths. If you, the reader, want to prove something, go ahead.

We need to put the Javascript into the template (or our menu will be unwantedly static). Here is everything you need, plus a theme, for the template head (or Media). So; JQuery, Django JQuery init, the menu JS code, the CSS base and theme, ::


    <script type="text/javascript" src={% static 'admin/js/vendor/jquery/jquery.min.js' %}></script>
    <script type="text/javascript" src={% static 'admin/js/jquery.init.js' %}></script>
    <script src={% static 'django_menus/js/django_menu.js' %}></script>
    <link href={% static 'django_menus/django_menu_base.css' %} type="text/css" media="all" rel="stylesheet">
    <link href={% static 'django_menus/django_menu_professional_sale.css' %} type="text/css" media="all" rel="stylesheet">            
  
Phew. Now, easy, as this is a vertical pushdown menu (the default), ::

        <ul class="dmenu dmenu-js dm-prsale">

PS: a pushdown stacking menu seems to be commonly agreed as one of the best solutions for a responsive design.

I built this theme, and I'm sure it could make some people happy,

.. figure:: https://raw.githubusercontent.com/rcrowther/django_menus/master/docs/images/ps_menu.png
    :width: 160 px
    :alt: menu screenshot
    :align: center


It's not my idea of good, though. It probably needs to go in an overlay or something.

  
Tabs
~~~~
Tabs are a web concept which seem to be vanishing nowadays. I suspect the need for responsive design is pushing designers towards stacked displays?

Anyway, the idea is that a site displays big objects across pages, not in hard-to-digest one-page lumps. URLs like, ::

    /product/1/detail
    /product/1/spec
    /product/1/comments
    
    /product/2/detail
    /product/2/spec
    /product/2/comments
 
Then the site uses relative URLs to access (another way is a Javascript hide, but this has accessibility issues).

To configure a tab menu is the same as usual, but with relative URLs e.g. ::

    'PRODUCT_TABS': [
        URL("product", "product"),
        URL("spec", "spec"),
        URL("comments", "comments"),
    ],

That simple. And the menu will navigate from one URL to another.

However, there are some style issues. First, if you want 'select' on such a menu, it will need to match against the tail of the URL (to match the relative URLs used in the config above). Then the menu needs some unusual CSS styling. Django_menus has a theme to try, ::

    <link href={% static 'django_menus/django_menu_base.css' %} type="text/css" media="all" rel="stylesheet">
    <link href={% static 'django_menus/django_menu_desktop_tabs.css' %} type="text/css" media="all" rel="stylesheet">

        <ul class="dmenu dmenu-horizontal dm-dttabs">


        {% get_menu "site/PRODUCT_TABS?trail_key=TAIL1;select_leaf=True" as product_tabs %}
        
Note that no action CSS files are declared because there is only only level of links (if you want multi-level tabs, go do it). Looks like this,

.. figure:: https://raw.githubusercontent.com/rcrowther/django_menus/master/docs/images/desktop_tabs.png
    :width: 160 px
    :alt: tabs screenshot
    :align: center

An aside: if you remove 'dmenu-horizontal' then the tabs become a downward stack. In other words, a natural start for responsive design (though I've never found a tabs-into-responsive-stack design on the web).



.. _NiceMenus: https://www.drupal.org/project/nice_menus

