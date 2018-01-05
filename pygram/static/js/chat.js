
jQuery(document).ready(function(){
    chat.init();

    jQuery('#comment').emojiPicker({
        width: '300px',
        height: '200px',
        button: false,
        onShow: function(picker, settings, isActive) {
            if(isActive == true){
                /*setTimeout(function(){
                    jQuery(".emojiPicker").css('cssText', 'top: 100px !important');
                }, 500);*/
            }

        }
    });

    jQuery('.reply-emojis').click(function(e) {
        e.preventDefault();
        jQuery('#comment').emojiPicker('toggle');
    });
});

var ucitavanje, newmsg = 0, request;
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

    createConversation : function(id){
        jQuery.ajax({
            method: "POST",
            url: "/ajax/createconversation/" + id,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            },
            success: function(response){
                chat.loadConversations();
                chat.openChat(response);
            }
        });
    },

    setTabTitle : function(){
        jQuery(window).on("blur focus", function(e) {
            var prevType = $(this).data("prevType");

            if (prevType != e.type) {   //  reduce double fire issues
                switch (e.type) {
                    case "blur":
                        document.title = "(" + newmsg + ") New Message!"
                        break;
                    case "focus":
                        newmsg = 0;
                        document.title = "Chat Module"
                        break;
                }
            }

            jQuery(this).data("prevType", e.type);
        })
    },

    sendMessage : function(){
        message = jQuery("#comment");
        chat_id = jQuery(".chathead").attr("id");
        if(message.val() == ""){

        } else {
            jQuery.ajax({
                method: "POST",
                url: "/ajax/sendmessage/",
                data: {"message": message.val(), "idconv": chat_id},
                csrfmiddlewaretoken: window.CSRF_TOKEN,
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
                    jQuery("#comment").val('');
                },
                success: function (response) {
                }
            });
        }
    },

    getMessages : function(callback){
        if(request){
            request.abort()
        }
        last_id = jQuery(".row.message-body").last().attr("id");
        if(last_id == undefined){
            last_id = "1"
        }
        chat_id = jQuery(".chathead").attr("id");
        request = jQuery.ajax({
            method: "POST",
            url: "/ajax/getnewmessages/" + chat_id + "/" + last_id,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            },
            success: function(response){

                if(response != "" ){

                    jQuery("#conversation").append(response).fadeIn();

                    jQuery("#conversation").animate({ scrollTop: $("#conversation").prop("scrollHeight") }, 500);
                }
                ucitavanje = setTimeout(callback,500);
                chat.loadConversations();

            }
        });


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
        clearTimeout(ucitavanje);
        jQuery.ajax({
            method: "POST",
            url: "/ajax/loadchat/" + id,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
                jQuery(".chat-load").html(' ');
            },
            success: function(response){
                jQuery(".chat-load").hide().html(response).fadeIn();
                chat.loadMessages(id);
                jQuery("#conversation").animate({ scrollTop: $("#conversation").prop("scrollHeight") }, 500);
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
                chat.loadConversations();
            }
        });
    }
}
