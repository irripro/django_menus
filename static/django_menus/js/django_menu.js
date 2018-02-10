(function($){
    'use strict';
    $(document).ready(function() {
      /*alert( "JS called." ); */

        /* initially set submenus on or off */
        var l = $(".dmenu-js .submenu")
        l.each(function(idx, sm) {
          var m = $(sm)
          var c = $(m.children('ul')[0])
          if (m.hasClass("expanded")) {
            c.css("display", "block") 
          } else {
            c.css("display", "none") 
          }
        })
        
        /* toggle expand, sliding up/down */
        $(".dmenu-js .submenu").click(function(e) {
            var sm = $(this)
            var c = $(sm.children("ul")[0])
            if(sm.hasClass("expanded")) {
                sm.removeClass("expanded")
                c.slideUp("fast")
            } else {
                sm.addClass("expanded")
                c.slideDown("fast")
             }
            e.stopPropagation()
        });
    });
})(django.jQuery);
