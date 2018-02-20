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
    If you want to change colors/font-size, padding etc. No maintenance.

Change direction of menu
    If you use built-in CSS, easy. Add the appropriate classes. No maintenance.

Insert new items to menus
    Producing a new item is easy, look in .items.py. Rendering it currently involves overriding the attribute 'handlers' in a Menu(). This is also easy. No maintainence.
    
Modify structure of HTML
    Currently, the app does not implement a templating system for the HTML. It uses string templates located in Itemviews. Override the template attribute in an ItemView. Even better, make a new ItemView with the new template. No maintainence.


  
Fun things you can do
~~~~~~~~~~~~~~~~~~~~~
- Translucent menu
- Get some CSS animation going
(why, why do I even suggest this?)

