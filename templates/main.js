// // When the user scrolls down 20px from the top of the document, slide down the navbar
// // When the user scrolls to the top of the page, slide up the navbar (50px out of the top view)
// window.onscroll = function() {scrollFunction()};

// function scrollFunction() {
//   if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
//       document.getElementById("navbar").style.top = "0";
//   } else {
//       document.getElementById("navbar").style.top = "-50px";
//   }
// }

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
        localStorage.setItem("path", JSON.stringify(data));
        localStorage.setItem("currentStep", 0);
        localStorage.setItem("numDirections", data.length);

    }).catch(err => {

        // Do something for an error here
        console.log("Error with getting path to destination.")

    });
}


// return a string for the curr direction to be spoken
function getCurrDirection(){
    var currStep = parseInt(localStorage.getItem("currentStep"));

    if (currStep >= parseInt(localStorage.getItem("numDirections"))){
        // go to end route screen
        return " You have arrived at your final destination. Double tap the middle of your screen to end route.";
    }
    else {
        var currDir = JSON.parse(localStorage.getItem("path"))[currStep];
        var currBearing = currDir["direction"]["degrees"].toFixed(0) + " " + currDir["direction"]["bearing"];
        var currDist = (currDir["distance"]["miles"] * 1609.344).toFixed(0) + " meters";
        var output = " Direction begins now. Head " + currBearing + " for " + currDist + ". Direction end.";
        return output;
    }
}


// function that speaks the current direction
function speak() {

    // speech synthesis
    // https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#demo
    var synth = window.speechSynthesis;

    var defaultTxt = "When you have arrived at your destination, double tap the middle of your screen.";
    var voiceSelect = "en-US";

    var pitch = 1;
    var rate = 0.9;

    var voices = synth.getVoices();
  
    // utterThis is a speech synthesis utterance object
    var inputTxt = defaultTxt + getCurrDirection();
    console.log(inputTxt);
    var utterThis = new SpeechSynthesisUtterance(inputTxt);

    // set the voice to en-US
    for (var i = 0; i < voices.length; i++){
        if (voices[i].lang == voiceSelect){
            utterThis.voice = voices[i];
        }
    }

    // set the pitch and rate
    utterThis.pitch = pitch;
    utterThis.rate = rate;

    // speak it!
    synth.speak(utterThis);

    // utterThis.onpause = function(event) {
    //     var char = event.utterance.text.charAt(event.charIndex);
    //     console.log('Speech paused at character ' + event.charIndex + ' of "' +
    //     event.utterance.text + '", which is "' + char + '".');
    // }
}

var mylatesttap;
function doubletap() {

   var now = new Date().getTime();
   var timesince = now - mylatesttap;

   if((timesince < 600) && (timesince > 0)){

        // if still iterating through directions, increment the currentStep and speak the next direction
        if (parseInt(localStorage.getItem("currentStep")) < parseInt(localStorage.getItem("numDirections"))){
            console.log("double tap");
            localStorage.setItem("currentStep", 1+parseInt(localStorage.getItem("currentStep")));
            speak();
        }

   } else{
        // too much time to be a doubletap
        console.log("single tap");
    }

   mylatesttap = new Date().getTime();

}
