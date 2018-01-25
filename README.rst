Django Menus
============
A menu generator for Django applications.

Uses a hard coded base. As the author of another Django app wrote, "Who wants to use Admin to maintain menus?" (several applications use this approach).



Alternatives
------------

Category apps
+++++++++++++
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

https://pypi.python.org/pypi/django-menu-generator/1.0.2
https://github.com/un33k/django-menuware

There are also some hints taken from the Drupal module NiceMenus_.


Current state
-------------
As it arrives. Not working.



Usage
-----

Menus have no surrounding div, ul, or table tags. These need adding, something like this, ::

    {% load menu_generator %}

    {% get_menu "NAV_MENU_LEFT" as site_menu %}
    <ul>
      {{ site_menu }}
    </ul>
 
Modifying
---------
These kinds of apps, this kind of code, has a habit of stating, "You can do anything with our code!" This app is for Django, an MVC framework, so this is true. But there is a limit beyond which you are hacking the app, not configuring. Pehaps the following will help...


Menu HTML structure
~~~~~~~~~~~~~~~~~~~
Menus render,

Some additions to 'class' are hard-coded. These are,


.. _NiceMenus: https://www.drupal.org/project/nice_menus

