$(document).ready(function () {

    $('.deleteItem').submit(function () {
        const action_url = $(this).attr('data-action-url');
        if (confirm('Are you sure you want to delete this listing?')) {
            this.action = action_url;
        }
    });

});