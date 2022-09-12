let map;
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 52.237049, lng: 21.017532 },
        zoom: 2,
    });
}
window.initMap = initMap;
