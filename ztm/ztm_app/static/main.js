//Zapisanie miejsca transakcji w przeglądarce
function setPlace() {
    var id = document.getElementById("selectPlace").value;
    console.log("HENLO")
    var place = new Object();
    place.id = id
    window.localStorage.setItem("place", JSON.stringify(place));
  }

function setTicketType(){
    console.log('type',d)
    //var type = new Object();
    place.type = "1"
    window.localStorage.setItem("place", JSON.stringify(place));
}

function setReduction(r){
    console.log('reduction', r)
    var reduction = new Object();
    reduction.value = r
    window.localStorage.setItem("reduction", JSON.stringify(reduction));
}