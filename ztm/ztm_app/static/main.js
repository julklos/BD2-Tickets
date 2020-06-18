//Zapisanie miejsca transakcji w przeglądarce
function setPlace() {
    window.localStorage.clear();
    var id = document.getElementById("selectPlace").value;
    var place = new Object();
    place.id = id
    window.localStorage.setItem("place", JSON.stringify(place));
    
  }

  function getCookie(c_name)
{
  if (document.cookie.length > 0) {
    c_start = document.cookie.indexOf(c_name + "=");
    if (c_start != -1) {
      c_start = c_start + c_name.length + 1;
      c_end = document.cookie.indexOf(";", c_start);
      if (c_end == -1) c_end = document.cookie.length;
      return unescape(document.cookie.substring(c_start,c_end));
    }
  }
  return "";
}

  $(document).ready(function() {
    $.ajaxSetup({
      headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
  });
  
function setTicketList(){
        var tickets= new Object();
        tickets.items = [];
        window.localStorage.setItem("tickets", JSON.stringify(tickets));
        
      
}
function storeTickets(tickets) {
    window.localStorage.setItem("tickets", JSON.stringify(tickets));
}
function loadTickets() {
    return JSON.parse(window.localStorage.getItem("tickets"));
  }
function setTicketType(d){
    tickets = loadTickets();
    if(!tickets){
        var tickets= new Object();
        tickets.items = []
        console.log('here')
    }
    console.log(d, tickets)
    var item = new Object();
    item.type = d
    tickets.items.push(item);
    storeTickets(tickets);
   
}
function setAmount() {
    var value =  document.getElementById("selectAmount").value;
    tickets = loadTickets();
    var last = tickets.items.pop()
    last.amount = value
    tickets.items.push(last);
    storeTickets(tickets)
}

function setReduction(r){
    tickets = loadTickets();
    var last = tickets.items.pop()
    last.reduction = r
    tickets.items.push(last);
    storeTickets(tickets)
}

function setClient(id_p){
  tickets = loadTickets();
  var last = tickets.items.pop()
  last.client = id_p;
  tickets.items.push(last);
  storeTickets(tickets)
}

function setCard(id_c){
  tickets = loadTickets();
  var last = tickets.items.pop()
  last.card = id_c;
  tickets.items.push(last);
  storeTickets(tickets)
}

function pay(id){
    const data = {
        payment : id,
        place : JSON.parse(window.localStorage.getItem('place')).id,
        items: JSON.parse(window.localStorage.getItem('tickets')).items,
    }
    console.log(id,data)
    sendTransactionRequest(data, function(response) { // success
        alert("Zamówienie złożone pomyślnie!");
       console.log(response)
      }, sendOrderError);
}

function payCard(id){
  const data = {
      payment : id,
      place : JSON.parse(window.localStorage.getItem('place')).id,
      items: JSON.parse(window.localStorage.getItem('tickets')).items,
  }
  console.log(id,data)
  sendTransactionRequestCard(data, function(response) { // success
      alert("Zamówienie złożone pomyślnie!");
     console.log(response)
    }, sendOrderError);
}

function sendTransactionRequest(info, onSuccess, onError)
{
  $.ajax(
    { url: '/transactionCarton'
    , success: onSuccess
    , data: JSON.stringify(info)
    , contentType: 'application/json'
    , error: onError
    , type: 'POST'
    });
}

function sendTransactionRequestCard(info, onSuccess, onError)
{
  $.ajax(
    { url: '/transactionCard'
    , success: onSuccess
    , data: JSON.stringify(info)
    , contentType: 'application/json'
    , error: onError
    , type: 'POST'
    });
}

function sendOrderError(xhr, textstatus) {
    alert("BŁĄD");
  }