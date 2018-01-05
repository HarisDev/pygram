jQuery(document).ready(function(){
   friends.init();
});
var request;
var friends = {

    init : function(){
        jQuery("#search-name").keyup(function(e){
            if(jQuery(this).val().length > 0){
                friends.searchUsers(jQuery(this).val());
            }
        })
    },

    searchUsers : function(text){
        if(request){
            request.abort();
        }
        request = jQuery.ajax({
           method: "POST",
           url: "/ajax/search/",
           data: {text: text},
           csrfmiddlewaretoken: window.CSRF_TOKEN,
           beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            },
           success: function(response){
                jQuery(".populate-users").html(response);
           }
        });
    },

    addFriend : function(id){
        jQuery.ajax({
            method: "POST",
            url: "/ajax/addfriend/"+id,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            },
            success: function(response){
                jQuery("#add-" + id + " .addf").html("Added!");
            }
        });


    },

    accept : function(id){
        jQuery.ajax({
            method: "POST",
            url: "/ajax/accept/"+id,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            },
            success: function(response){
                jQuery("#request-" + id + " ").fadeOut();
            }
        });
    },

    decline : function (id) {
        jQuery.ajax({
            method: "POST",
            url: "/ajax/decline/"+id,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            },
            success: function(response){
                jQuery("#request-" + id + " ").fadeOut();
            }
        });
    }

}