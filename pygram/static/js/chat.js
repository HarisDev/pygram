
jQuery(document).ready(function(){
    chat.init();
});

chat = {
    init : function (){
        this.loadConversations();
        this.addEnterListener();
    },

    addEnterListener : function(){
        jQuery("#comment").keypress(function(e){
            if(e.which == 13){
                chat.sendMessage();
            }
        })
    },

    sendMessage : function(){
        message = jQuery("#comment");
        chat_id = jQuery(".chathead").attr("id");
        jQuery.ajax({
            method: "POST",
            url: "/ajax/sendmessage/",
            data: { "message": message.val(), "idconv": chat_id},
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
                jQuery("#comment").val('');
            },
            success: function(response){
            }
        });
    },

    getMessages : function(callback){
        last_id = jQuery(".row.message-body").last().attr("id");
        if(last_id == undefined){
            last_id = "1"
        }
        chat_id = jQuery(".chathead").attr("id");
        jQuery.ajax({
            method: "POST",
            url: "/ajax/getnewmessages/" + chat_id + "/" + last_id,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            },
            success: function(response){
                if(response != ""){
                    jQuery("#conversation").append(response).fadeIn();
                }

            }
        });

        setTimeout(callback,1000);
    },

    startChatListener : function(){
        (function getChatsTimeoutFunction(){
            chat.getMessages(getChatsTimeoutFunction);
        })();
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
    },

    openChat : function(id){
        jQuery.ajax({
            method: "POST",
            url: "/ajax/loadchat/" + id,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            },
            success: function(response){
                jQuery(".chat-load").hide().html(response).fadeIn();
                chat.loadMessages(id);
            }
        });
    },

    loadMessages : function(id){
        jQuery.ajax({
            method: "POST",
            url: "/ajax/loadmessages/" + id,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            },
            success: function(response){
                jQuery("#conversation").hide().html(response).fadeIn();
                chat.startChatListener();
            }
        });
    }
}
