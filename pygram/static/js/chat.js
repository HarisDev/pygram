
jQuery(document).ready(function(){
    chat.init();
});

chat = {
    init : function (){
        this.loadConversations();
    },

    loadConversations : function(){
        jQuery.ajax({
            method: "POST",
            url: "/ajax/loadconversations/",
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            },
            success: function(response){
                jQuery(".conversations").html(response);
            }
        });
    }
}
