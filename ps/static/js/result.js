let allListings = [
    {
        plantId: '1',
        plantType: 'Rose',
        imagePath: '../static/media/img/plants/Rose.jpeg',
        distance: 10,
        description: 'Rose cutting'
    },
    {
        plantId: '2',
        plantType: 'Rose',
        imagePath: '../static/media/img/plants/Rose.jpeg',
        distance: 30,
        description: 'Rose cuttings1'

    },
    {
        plantId: '4',
        plantType: 'Outdoor',
        imagePath: '../static/media/img/plants/Rose.jpeg',
        distance: 15,
        description: 'Rose cutting2'
    }
]
var defaultSearchText = '';
$(document).ready(function () {
    defaultSearchData();
});


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

        imgTag.onclick = function () {
            $('.close').click(function () {
                divModalTag.style.display = "none";
            });
            divModalTag.style.display = "block";
            divModalTag.children[1].setAttribute("src", this.getAttribute("src"));
            divModalTag.children[1].setAttribute("alt", this.getAttribute("alt"));
        }

        var divModalTag = document.createElement("div");
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
        $('.search-table tbody').append(trNode);

    }
}