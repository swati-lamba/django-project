$(document).ready(function () {

    $(document).on("click", "#delete-comment a" , function(event) {
        event.preventDefault();
        var isSuccess= false;
        let ajax_url = this.href;
        $.ajax({
            url: ajax_url,
            data: {},
            type: "POST",
            dataType: "json",
            headers: {'X-CSRFToken': csrftoken},
            })
            .done(function (json) {
                if(json.success != true){
                    alert("Some error occurred, please retry!")
                } else {
                   var ele = $( 'div[data-comment-id="'+json.comment_id+'"]');
                    ele.remove();
                }
            })
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            })
            .always(function (xhr, status) {
            });
        });

    $(document).on("click","#edit-comment a", function (event) {
        event.preventDefault();
        let ajax_url = this.href;
        var comEle = $( 'div[data-comment-id="'+$(this).attr('data-c-id')+'"]').children('.comment-text');
        var comment_text = comEle.text();
        comEle.html('<input type="textarea" value=\"' + comment_text + '\" rows="6" cols="50">');
        var updateBtn = document.createElement("button");
        updateBtn.class="update-comment"
        updateBtn.innerHTML="Update"
        updateBtn.onclick = function () {
            var newVal = $(this).parent().children('input').val();
            $.ajax({
            url: ajax_url,
            data: { "comment" : newVal },
            type: "POST",
            dataType: "json",
            headers: {'X-CSRFToken': csrftoken},
            })
            .done(function (json) {
                if(!json.success){
                    alert("Some error occurred, please retry!")
                } else {
                     comEle.html(newVal);
                }
            })
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            })
            .always(function (xhr, status) {
            });
        }
        comEle.append(updateBtn)
        var cancelBtn = document.createElement("button");
        cancelBtn.class="cancel-comment"
        cancelBtn.innerHTML="Cancel"
        cancelBtn.onclick = function () {
           // $(this).parent().children().remove();
            $(this).parent().html(comment_text);
        }
        comEle.append(cancelBtn)
    });

    $('.new-comment').submit(function (event) {
        event.preventDefault();
        var ajax_url = this.action;
        var comment_text = document.getElementById("newComment").value;

        $.ajax({
            url: ajax_url,
            data: { "comment" : comment_text },
            type: "POST",
            dataType: "json",
            headers: {'X-CSRFToken': csrftoken},
        })
            .done(function (json) {
                document.getElementById("newComment").value = '';
                var node = document.createElement("div");
                node.setAttribute("data-comment-id",json.comment_id)
                node.innerHTML = ' <a href='+json.profile_url+'>You</a> posted:<div class="comment-text">'+ comment_text+'</div> a few seconds ago<div id="edit-comment">Click to <a data-c-id="'+json.comment_id + '" href="'+json.edit_url+'">edit the post</a></div><div id="delete-comment">Click to <a href='+json.delete_url+'>delete the post</a></div>';
                document.getElementById("all-comments").prepend(node);
            })
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            })
            .always(function (xhr, status) {
            });
    });

});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');