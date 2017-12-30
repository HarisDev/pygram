
jQuery(document).ready(function(){
    alert('{{ csrf_token }}');
    jQuery.ajax({
        method: "POST",
        url: "/ajax/loadconversations/",
        csrfmiddlewaretoken: '{{ csrf_token }}',
        success: function(response){
            alert("Works! " + response);
        }
    })
});
