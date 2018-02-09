(function($){
    'use strict';
    $(document).ready(function() {
      /*css( "background-color", "red" )*/
        $("dmenu").find(".ul").css( "display", "none" )     
        /* needs to toggle */
        $("dmenu").find(".submenu").click(function(ev) {
            alert( "Handler for .click() called." );
            ev.target.children(".ul").css( "display", "block") 
        });
    });
})(django.jQuery);
