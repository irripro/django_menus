Django Menus
============
A menu generator for Django applications.

Uses a hard coded base. As the author of another Django app wrote, "Who wants to use Admin to maintain menus?" (a few other applications use this approach).

By default, the app renders menu data as CSS-only hover-action dropdown menus. There are also files/support for creating one-click JavaScript menus. The HTML output is data with no action enabled, so can be used to enable whatever style and action of menu you want.

When to use
~~~~~~~~~~~
This is a sophisticated version of a menu builder. It has an API with similarities to django.Form. Why use a powerful (probably hungry?) app like this? For a simple menu you should not. In Django you can nake a menu in a template by writing in the links, then move or change the menu with a simple rewrite.

The time to use this app is when you want long-term maintainability. To be able to come back after a year and know how to make substancial changes in minutes. Or when you have a deep menu system and your templates are becoming cluttered and hard to read.

There are minor reasons also. If you are looking for fancy menus, but are not using front-end bundles like Bootstrap, this app has front-end theming that will get you close quickly. Some of the themes are close to responsive displays; you will only need to style a suitable wrap in the template.  

The app also provides some actions that would be tedious or difficult otherwise. You may have a small menu, but if you would like to auto-expand to the current page, this app can do that.


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
Unlike much of my Django code, this app originated in other code, a Django application named 'menu-generator'. I do not have the technical knowhow nor computing capability to fork the project, so started again. 

The app is now nothing like the elegance of 'menu-generator'. It was rewritten to gather much of the API from Django Forms. So, Menu is like Form. Menu is populated with ItemHandlers (like Fields) which contain ItemViews (like Widgets).

However, while this will help explain the overall structure, be careful of comparing too closely. Menu is much simpler than Form. The app refines the purpose of ItemHandlers, so they are not like Fields and have important extra abilities. Probably best to say, knowing this app is like Django Forms means you may be able to guess what kind of features it offers and how to use them (for example, yes, you can make custom menu items. You can add special attributes to menu items of one type etc.).  

https://pypi.python.org/pypi/django-menu-generator/1.0.2
https://github.com/un33k/django-menuware

Some hints are taken from the Drupal module NiceMenus_. And the old Drupal router.


Current state
-------------
As it arrives. No guarentees.


Installation
------------
Place the app in a Django environment. In settings.py, ::

    INSTALLED_APPS = [
        ...
        'django_menus',
    ]

Done (there are various minor reasons why this app likes to be declared).


Usage
-----

Menus have no surrounding div, ul, or table tags. These need adding, something like this, ::

    {% load menu_generator %}

    {% get_menu "NAV_MENU_LEFT" as site_menu %}
    <ul>
      {{ site_menu }}
    </ul>
        
        
Quickstart
----------
Build a menu  configuration in an app. Put it in a file 'menubase.py'. The menu is a dict containing classes, and the dict name must be 'MENUS'. Here's an example, ::
    
    from django_menus import SubMenu, URL, Separator
    
    MENUS = {
        'NAV_MENU_TOP_DEPARTMENTS': [
            URL("Classics", "/classics/"),
            URL("Sociology", "/sociology/"),
            URL("Fine Art", "/fineart/"),
        ]
        'NAV_MENU_TOP_WORK_WITH_US': [
            URL("Help", "/help/"),
            URL("By department", "/department/conferences/"),
            URL("Conferences", "/conferences/"),
            Separator(),
            URL("Contact", "/contact/"),
        ],    
        'NAV_MENU_TOP_RESOURCES': [
            URL("Map", "/map/"),
            URL("Plant", "/plant"),
            URL("Research", "/research"),
            URL("Events", "/conferences/"),
            URL("Projects", "/projects/"),
        ], 
        'NAV_MENU_TOP_ABOUT': [
            URL("Dates", "/dates/"),
            URL("Annual Report", "/report/annual/"),
            URL("Jobs", "/jobs/"),
        ],
        'NAV_MENU_TOP': [
            URL("Home", "/home/"),
            SubMenu("Departments", "#", 'NAV_MENU_TOP_DEPARTMENTS'),
            SubMenu("Work with us", "#", 'NAV_MENU_TOP_WORK_WITH_US'),
            SubMenu("Resources", "#", 'NAV_MENU_TOP_RESOURCES'),
            SubMenu("About", "#", 'NAV_MENU_TOP_ABOUT'),
            URL("Search", "/search/"),
        ]
    }
  

...

Data Structure
--------------
Menubase has a structure like above. You can find the definitions in the items.py. Use a MenuManager to recover menu data, ::

    MenuManager(self, app, menu_name)
    
There's not much more to say about that. The manager is placed in a...


Menu
~~~~~
Handles overall menu construction. Which means storage, validation, and rendering. Output can be as DIV or LI. Call str() and Menu outputs with the default, LI.

Menu also builds what are called 'URL trails'. Any menu item data which contains a 'url' attribute is checked, and the path noted in a dict of paths. Matching the end point of these trails against requests, Menu can guess if the current page is in the menu. If it is, menu can add classes to display that item in various ways.

This behaviour is not often used in desktop GUIs, but popular in web GUIs. It has advantages, especilly in long menus of content ('you (the user) are currently at page ...').



Options
+++++++
disable_invalid
    If true, and a menu item fails validation, it is not hidden (the 
    default) but 'greyed out' and anchor menu items are nulled (similar 
    to a desktop GUI showing non-applicable actions). 
expand_trail
    If True, and the current page can be found in the trails (however 
    deep it is nested), the menu is expanded to show that item.
select_trail
    If True, and the current page can be found in the trails (however 
    deep it is nested), the menu has 'select' styling on the trail items.
select_leaf
    If True, and the current page can be found in the trails (however 
    deep it is nested), the menu has 'select' styling on the target item.


Modifying
---------
These kinds of apps, this kind of code, has a habit of stating, "You can do anything with our code!" This app is for Django, an MVC framework, so this is true. But there is a limit beyond which you are hacking the app, not configuring. Perhaps the following will help.


Menu HTML structure
~~~~~~~~~~~~~~~~~~~~~~~
Menus may render as default (as_list()) as, ::

    <ul class="dmenu dmenu-right">
        <li><a href="/articles">Articles</a></li>
        <li class="submenu selected"><a href="#">About</a>
            <ul><li class="expanded"><a href="/contact">Contact</a></li>
            <li class="submenu"><a href="#">Credits</a><ul>
            <li class="selected"><a href="/credits/now">Now</a></li>
            <li><a href="/credits/always">Always</a></li>
            </ul>
        </li>
        <li><a href="/login">Login</a></li>
    </ul>

Some additions to 'class' are hard-coded. These are,

selected
    item marked as part of the current URL

submenu
    item marked as a container for a submenu
    
icon
    item marked as the icon image tag

expanded
    open this branch whatever the GUI state
    
disabled
    item marked as visible but not active



Menu item HTML/CSS structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mainly applies to the URL(), though some comments also to SubMenu(), ::

    <li class=""><a href="/login"><img class="icon"/>Login</a></li>

The "icon" class is hard-coded.

The structure is unusual, and has implications for CSS. First, you will see that the method of placing icons is an image tag. For many years the usual technique was some padding and a background image, or maybe an inserted DIV. The disadvantage of IMG is that you can not use CSS to place content ::before or ::after. So the wonderful Unicode symbols can not be used. The advantage is that the tag is semantic, and can be reliably sized. A fixed width will space the link text into a column; the only work needed is to set a margin (not padding) on all "menu-item-icon" IMGs.

Second, there is no injected HTML/text to help with placing items to the right. This is because CSS still has no good way of handling this layout ('flexbox' has been massively promoted. Hummm). But the ancient background-image technique is good (especially as django-menu uses a written block to handle left icons), e.g. ::

    background-image: url('/static/django_menus/icons/black_small_right_triangle.svg');
    background-position: right center;
    background-repeat: no-repeat;  
    
    
Things you can do, and not do
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CSS override
    If you want to change colors/font-size, padding etc. See the next section. No maintenance.

Change direction of menu
    If you use bult-in CSS, easy. Add the appropriate classes. No maintenance.

Insert new items to menus
    Producing a new item is easy, look in .items.py. Rendering it currently involves modifying Menu() in .menu_handler.py. This is also easy. Not maintainable.
    
Modify structure of HTML
    Currently, the app does not implement a templating system for the HTML. This makes the app easy to read and maintain, but means changing the HTML is a hardcode override. Not maintainable.



Default CSS, themes, and overriding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Django menu comes with a CSS/JS action and theme set builtin.

I suppose I could claim how fabulous this is, which it can be. However, I've not worked it through. It can give strange and marvelous results. But give it a go because, if it gets you part-way down the road, that's a start, right?
 
WARNING
+++++++
The app includes little CSS files. They may be small, but they are advanced. Styling a CSS menu is not simple. For example, the menu needs space before item text. But most menus do not need spacing before top-level horizontal items (no icons there, usually). You can, to add space, set a width on the embedded icon IMG. To avoid the top level, you can select the horizontal menu, and kill spacing, or select only submenus to space, or go down a level e.g. .dm-desktop ul .menu-item-icon {width: 14px; margin: 0 2px;}.

Anchors often have browser styling, and need direct selection. If you want to customize a submenu mark, it's a background image, and you need a .png at least, which can be difficult to position without 'vertical-align'. If borders are added to items, the alignment will walk up and down, depending on the box-model. 

A theme that enables full support for django_menus will need to respond to 'selected' and 'expanded' classes, and have left/right/down variants.

You may work faster if you copy and modify. If you do not do this as a day job, it can take considerable time.


After warning
+++++++++++++
The menu tags, or a context injection, deliver a pre-rendered menu HTML. This, in a browser, looks promising (if you are a glass-half-full person) but is not finished product.

django_menus comes with a CSS/JS structure, and some themes, built-in. You can ignore all of this and roll your own. The CSS/JS can be hardcoded into templates, or delivered by Media statements (as used by Django Forms). You can keep as much as you want, or override.

Let's stay with the builtin system.

First, a template needs, ::

    {% load static %}

    <link href={% static 'django_menus/django_menu_base.css' %} type="text/css" media="all" rel="stylesheet">

Either via '{{ media }}' or, as above, a direct import.

django_menu_base.css delivers basic positioning for a menu. Say a menu 'SITE_MENU' is arriving in a template. Use the 'get_menu' filter, surround with the outside UL tags, ::

        {% load menu_generator %}

        {% get_menu "SITE_MENU" as site_menu %}
        <ul>
          {{ site_menu }}
        </ul>
        
If you have a look, the menu output is raw, but promising. Now import the CSS as described above, and add these classes to the wrapping UL tags, ::

        {% load menu_generator %}

        {% get_menu "SITE_MENU" as site_menu %}
        <ul class="dmenu dmenu-css dmenu-right dmenu-horizontal">
          {{ site_menu }}
        </ul>        
        
Any depth in the menu will disappear (which is correct, don't panic).

'dmenu' sets some known basics (e.g. "submenus do not initially show"). 'dmenu-css' sets CSS show-on-hover action. 'dmenu-right' opens submenus to the right ('dmenu-left' to the left). 'dmenu-horizontal' sets the first entries in the menu horizontal (or do not put this in, and have a vertical menu).

You can mix these CSS modules (though they can give wierd results). No directions gives a push-down menu stack, ::

        {% load menu_generator %}

        {% get_menu "SITE_MENU" as site_menu %}
        <ul class="dmenu dmenu-css">
          {{ site_menu }}
        </ul>  
        
Anyway, the menu looks tidier. More importantly, if you hover elements, you will find the menu operates as you asked. But it looks... basic. The menu may open in wild positions (these classes set no widths/heights/borders etc.).

You can add your own CSS, via Media or directly. Or you can have a look at the sample themes. Themes are in django_menu/static/... Add this to load one, ::

    <link href={% static 'django_menus/django_menu_desktop.css' %} type="text/css" media="all" rel="stylesheet">

Then add the class inside the file to the wrapping UL tags, ::

        {% load menu_generator %}

        {% get_menu "SITE_MENU" as site_menu %}
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

    {% get_menu "SITE_MENU" as site_menu %}
    <ul class="dmenu dmenu-css dm-machinery">
      {{ site_menu }}
    </ul> 

So,

.. figure:: https://raw.githubusercontent.com/rcrowther/django_menus/master/docs/images/machinery_menu.png
    :width: 160 px
    :alt: menu screenshot
    :align: center
    
Maybe pushing it there, huh, son?


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

I built this, and I'm sure it could make many people happy. It's not my idea of good, though. So you get no picture.

  
  
Fun things you can do
~~~~~~~~~~~~~~~~~~~~~
- Translucent menu
- Get some CSS animation going
(why, why do I even suggest this?)


.. _NiceMenus: https://www.drupal.org/project/nice_menus

