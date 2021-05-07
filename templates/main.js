// When the user scrolls down 20px from the top of the document, slide down the navbar
// When the user scrolls to the top of the page, slide up the navbar (50px out of the top view)
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      document.getElementById("navbar").style.top = "0";
  } else {
      document.getElementById("navbar").style.top = "-50px";
  }
}

// script for getting user geolocation
var userLocation = document.getElementById("user-loc");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(storePosition);
    } else { 
        userLocation.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function storePosition(position) {
    userLocation.innerHTML = "Latitude: " + position.coords.latitude + "<br>Longitude: " + position.coords.longitude;
    
    localStorage.setItem('airport', 'ATL');
    localStorage.setItem('map', 'C');
    localStorage.setItem('destination', 'C33');
    localStorage.setItem('userLat', position.coords.latitude);
    localStorage.setItem('userLon', position.coords.longitude);

    console.log(localStorage.getItem('airport'));
    console.log(localStorage.getItem('map'));
    console.log(localStorage.getItem('destination'));
    console.log(localStorage.getItem('userLat'));
    console.log(localStorage.getItem('userLon'));
}

function makeDL(array){
  // Create the list element:
  var list = document.createElement("DL");

  for (var i = 0; i < array.length; i++) {

      // Create the list item:
      var item = document.createElement('DT');
      var description = "Head " + array[i]['direction']['degrees'].toFixed(0) + " " + array[i]["direction"]["bearing"]
      item.appendChild(document.createTextNode(description));

      var itemDescription = document.createElement("DD");
      var distance = (array[i]["distance"]["miles"] * 1609.344).toFixed(0);
      itemDescription.appendChild(document.createTextNode(distance + "m"));

      // Add it to the list:
      list.appendChild(item);
      list.appendChild(itemDescription);
      list.appendChild(document.createElement("HR"));
  }

  return list
}

// function to calculate path from user to destination
function calculatePath(){
    var apiUrl = 'https://disability-assist.herokuapp.com/api/path?lat=' + localStorage.getItem('userLat') + '&lon=' + localStorage.getItem('userLon') + '&airport=ATL&map=C&destID=C33';
    
    fetch(apiUrl).then(response => {
        return response.json();
    }).then(data => {

        // Work with JSON data here
        document.getElementById("directions").appendChild(makeDL(data));


    }).catch(err => {

        // Do something for an error here
        console.log("Error with getting path to destination.")

    });
}