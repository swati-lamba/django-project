let allListings = [
    {
        plantId: '1',
        plantType: 'Rose',
        imagePath: '../static/media/img/plants/roses.jpg',
        distance: 10,
        description: 'Rose cutting'
    },
    {
        plantId: '2',
        plantType: 'Rose',
        imagePath: '../static/media/img/plants/Rose.jpeg',
        distance: 30,
        description: 'Rose cuttings'

    },
    {
        plantId: '3',
        plantType: 'Snake',
        imagePath: '../static/media/img/plants/snake.jpeg',
        distance: 20,
        description: 'Low maintainance'
    },
    {
        plantId: '4',
        plantType: 'Indoor',
        imagePath: '../static/media/img/plants/plant1.jpeg',
        distance: 15,
        description: 'Green'
    }
]
var defaultSearchText = '';
$(document).ready(function () {
    $('.global-search').submit(function () {
        return setAction(this);
    });

    $('div input.search').click(function () {
        $(this).siblings(".clear").remove();
        var clearSearchResults = '<input type="submit" class="clear" value="Clear Results" onclick="clearFields()">';
        $(this).parent().append(clearSearchResults);
        $(".searchdata").remove();
        defaultSearchData();
    });
});

function clearFields() {
    var clearBtn = $('.clear');
    var selectedSearchItems = clearBtn.siblings('select');
    selectedSearchItems.children('.default').prop("selected", true);
    $(".searchdata").remove();
}

function defaultSearchData() {
    for (var data in allListings) {
        var tdPlantType = document.createElement("td");
        var plantType = document.createTextNode(allListings[data].plantType);
        tdPlantType.appendChild(plantType);

        var tdPlantImg = document.createElement("td");
        var imgTag = document.createElement("img");
        imgTag.setAttribute("src", allListings[data].imagePath);
        imgTag.setAttribute("width", 30);
        imgTag.setAttribute("height", 30);
        imgTag.setAttribute("alt", allListings[data].plantType);
        imgTag.setAttribute("id", "myImg");
        var divModalTag = document.createElement("div");
        imgTag.onclick = function () {
            $('.close').click(function () {
                divModalTag.style.display = "none";
            });
            divModalTag.style.display = "block";
            divModalTag.children[1].setAttribute("src", this.getAttribute("src"));
            divModalTag.children[1].setAttribute("alt", this.getAttribute("alt"));
        }
        divModalTag.setAttribute("id", "myModal");
        divModalTag.setAttribute("class", "modal");
        divModalTag.innerHTML = '<span class="close">&times;</span><img class="modal-content" id="img01"><div id="caption"></div>';
        tdPlantImg.appendChild(imgTag);
        tdPlantImg.appendChild(divModalTag);
        var tdPlantDist = document.createElement("td");
        var plantDist = document.createTextNode(allListings[data].distance);
        tdPlantDist.appendChild(plantDist);

        var tdPlantDesc = document.createElement("td");
        var desc = document.createTextNode(allListings[data].description);
        tdPlantDesc.appendChild(desc);

        var tdConnect = document.createElement("td");
        var aConnect = document.createElement("a");
        aConnect.setAttribute("href", "#");
        var imgConnect = document.createElement("img");
        imgConnect.setAttribute("src", "../static/media/img/misc/connect-icon.png");
        imgConnect.setAttribute("width", 30);
        imgConnect.setAttribute("height", 30);
        aConnect.appendChild(imgConnect);
        tdConnect.appendChild(aConnect);

        var trNode = document.createElement("tr");
        trNode.appendChild(tdPlantType);
        trNode.appendChild(tdPlantImg);
        trNode.appendChild(tdPlantDist);
        trNode.appendChild(tdPlantDesc);
        trNode.appendChild(tdConnect);
        trNode.setAttribute("class", "searchdata");
        $('.search-table tbody').append(trNode);
    }
}

function setAction(form) {
    if (form.firstElementChild.value !== 'rose') {
        tempAlert("No results found!", 4000);
        return false;
    }
    form.action = "results";
    return true;
}

function tempAlert(msg, duration) {
    var el = document.createElement("div");
    el.setAttribute("class", "alert");
    el.innerHTML = msg;
    setTimeout(function () {
        el.parentNode.removeChild(el);
    }, duration);
    document.body.appendChild(el);
}