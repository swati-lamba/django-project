$(document).ready(function () {
    $('body').on('click', '.editable', function () {
            if ($(this).attr('modified') !== 'true') {
                this.setAttribute('modified', 'true');
                var text = this.innerHTML;
                $(this).html('<input type="text" value=\"' + text + '\">');
            }
        }
    );

    $('body').on('keyup', '.editable', function (event) {
        if (event.key === 'Enter') {
            const save_url = $(this).attr('data-save-url');
            var updatedName = this.firstElementChild.value;
            var success = false;
            $.ajax({
                url: save_url,
                data: {"plant_name": updatedName},
                type: "POST",
                dataType: "json",
                headers: {'X-CSRFToken': csrftoken},
            })
                .done(function (json) {
                    if (json.success) {
                        success = true;
                    } else {
                        console.log(json.error);
                    }
                })
                .fail(function (xhr, status, errorThrown) {
                    alert("Sorry, there was a problem!");
                })
                .always(function (xhr, status) {
                });

            this.setAttribute('modified', 'false');
            this.firstElementChild.remove()
            this.innerHTML = updatedName;
        }
    });

    $('button.loadData').click(function () {
        const ajax_url = $(this).attr('data-ajax-url');
        const details_url = $('#my-listings').attr('data-details-url');
        const edit_url = $('#my-listings').attr('data-edit-url');
        const details_icon_path = $('#my-listings').attr('data-details-img');
        const edit_icon_path = $('#my-listings').attr('data-edit-img');
        const name_save_url = $('#my-listings').attr('data-name-save');

        $.ajax({
            url: ajax_url,
            data: {},
            type: "GET",
            dataType: "json",
            headers: {'X-CSRFToken': csrftoken},
        })
            .done(function (json) {
                var full_list = JSON.parse(json.list);
                $('#my-listings table tr td').remove();
                for (var i = 0; i < full_list.length; i++) {
                    var img = full_list[i].fields.name;
                    var desc = full_list[i].fields.description;
                    var loc = full_list[i].fields.distance;
                    var status = full_list[i].fields.status;
                    var plant_id = full_list[i].pk;
                    var editLink = getUrl(edit_url, plant_id);
                    var edit = '<a href=' + editLink + '><img alt="Edit" src=' + edit_icon_path + ' width="30" height="30"></a>'
                    var view = '<a href=' + getUrl(details_url, plant_id) + '><img alt="Details" src=' + details_icon_path + ' width="30" height="30"></a>'
                    var added_row = '<td class="editable" data-save-url=' + getUrl(name_save_url, plant_id) + '>' + full_list[i].fields.name + '</td>'
                        + '<td>' + img + '</td>'
                        + '<td>' + desc + '</td>'
                        + '<td>' + loc + '</td>'
                        + '<td>' + status + '</td>'
                        + '<td>' + edit + '</td>'
                        + '<td>' + view + '</td>';

                    var table = document.getElementById("myPlantTable");
                    var row = table.insertRow();
                    row.innerHTML = added_row;
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

    $('#sortByName').click(function () {
        const ajax_url = $(this).attr('data-ajax-url');
        const details_url = $('#my-listings').attr('data-details-url');
        const edit_url = $('#my-listings').attr('data-edit-url');
        const details_icon_path = $('#my-listings').attr('data-details-img');
        const edit_icon_path = $('#my-listings').attr('data-edit-img');
        const name_save_url = $('#my-listings').attr('data-name-save');

        $.ajax({
            url: ajax_url,
            data: {"sortBy": "name"},
            type: "GET",
            dataType: "json",
            headers: {'X-CSRFToken': csrftoken},
        })
            .done(function (json) {
                var full_list = JSON.parse(json.list);
                $('#my-listings table tr td').remove();
                for (var i = 0; i < full_list.length; i++) {
                    var img = full_list[i].fields.name;
                    var desc = full_list[i].fields.description;
                    var loc = full_list[i].fields.distance;
                    var status = full_list[i].fields.status;
                    var plant_id = full_list[i].pk;
                    var editLink = getUrl(edit_url, plant_id);
                    var edit = '<a href=' + editLink + '><img alt="Edit" src=' + edit_icon_path + ' width="30" height="30"></a>'
                    var view = '<a href=' + getUrl(details_url, plant_id) + '><img alt="Details" src=' + details_icon_path + ' width="30" height="30"></a>'
                    var added_row = '<td class="editable" data-save-url=' + getUrl(name_save_url, plant_id) + '>' + full_list[i].fields.name + '</td>'
                        + '<td>' + img + '</td>'
                        + '<td>' + desc + '</td>'
                        + '<td>' + loc + '</td>'
                        + '<td>' + status + '</td>'
                        + '<td>' + edit + '</td>'
                        + '<td>' + view + '</td>';

                    var table = document.getElementById("myPlantTable");
                    var row = table.insertRow();
                    row.innerHTML = added_row;
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

function getUrl(url, id) {
    return url.replace('0', id);
}