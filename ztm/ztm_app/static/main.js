//Zapisanie miejsca transakcji w przeglądarce
function setPlace() {
    window.localStorage.clear();
    var id = document.getElementById("selectPlace").value;
    var place = new Object();
    place.id = id
    window.localStorage.setItem("place", JSON.stringify(place));
    
  }

  function summary(){
      tickets = loadTickets()
      console.log('here',tickets)
      sum = tickets.items.reduce(function(acc, t) {
        return acc + (parseFloat(t.price)*parseFloat(t.amount)*parseFloat(t.reduction_val)/100);
      }, 0.0).toFixed(2);
      console.log(sum)
      sumHTML = tickets.items.map(function(item) {
        return genOneItemHtml( item.reduction_val, item.zone, item.price, item.time, item.amount);
      });
      sumHTML.join();
      
      console.log(sumHTML, sum)
      $("#tickettable").html(sumHTML);
    
      sum = genSumHtml(sum);
      $("#ticketsum").html(sum);
        
  }

  function genOneItemHtml(reduction, zone, price,time, amount) {
    var str = "<div class=\"row\"><div class=\"col-md-4\"><h6 class=\"product-name\"><strong> Czas ważności: ";
    str += time;
    str += " </strong></h6></div><div class=\"col-md-1\"><h6><strong>"
    str += price;
    str += "zł </strong></h6></div><div class=\"col-md-1\"><h6><span class=\"text-muted\">x </span>";
    str += amount;
    str += "</h6></div><div class=\"col-md-2\"><h6><span class=\"text-muted\"> Ulga: ";
    str += reduction;
    str +=" % </span></h6>strefa: <span class=\"badge badge-primary badge-pill\">";
    str += zone;
    str += "</span></div></div><hr>";
    return str;
  }
  
  
  function genSumHtml(sum) {
    var str = "<h4 class=\"text-center\">Łącznie <strong>";
    str += sum;
    str += "zł</strong></h4>";
    return str;
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
function setTicketType(d,t,s, p){
    var tickets = loadTickets();
    if(!tickets){
        var tickets= new Object();
        tickets.items = []
        console.log('here')
    }
    var item = new Object();
    item.type = d
    item.time = t
    item.zone = s
    item.price = p
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
    setUrlContinue()
}

function setReduction(r, val){
    tickets = loadTickets();
    var last = tickets.items.pop()
    last.reduction = r
    last.reduction_val = val
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

function setTicket(id_c){
  const data = {
    ticket : id_c,
  }
  console.log(id_c,data)
    sendActivationRequest(data, function(response) { // success
    alert("Aktywacja przebiegła pomyślnie!");
   console.log(response)
  }, sendOrderError);
}

function pay(id){
    var items = JSON.parse(window.localStorage.getItem('tickets')).items
    items = items.map(el=>{return({
        "reduction": el.reduction,
        "amount": el.amount,
        "type": el.type
    })})
    console.log(items, items[0])
    const data = {
        payment : id,
        place : JSON.parse(window.localStorage.getItem('place')).id,
        items: items,
    }
    console.log(id,data)
    sendTransactionRequest(data, function(response) { // success
        alert("Zamówienie złożone pomyślnie!");
       console.log(response)
       $("#tickettable").html();
       $("#ticketsum").html();
       $("#endSummary").html(response);
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

function sendActivationRequest(info, onSuccess, onError)
{
  $.ajax(
    { url: '/transactionActivation'
    , success: onSuccess
    , data: JSON.stringify(info)
    , contentType: 'application/json'
    , error: onError
    , type: 'POST'
    });
}

function sendTransactionRequest(info, onSuccess, onError)
{   var csrftoken = getCookie('csrftoken');
    var headers = new Headers();
    headers.append('X-CSRFToken', csrftoken); 
     $.ajax(
    { url: '/transactionCarton'
    , success: onSuccess
    , data: JSON.stringify(info)
    , contentType: 'application/json'
    , error: onError
    , type: 'POST'
    , headers: headers
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
  
function showStatAlert() {
  var stat = document.getElementById("selectStat").value;
  document.getElementById("wybrana_statystyka").innerText = `Wybrana statystyka: ${stat}`
}

function showStat() {
  var stat = document.getElementById("selectStat").value;
  if (stat == "brak") {
    alert("Nie wybrałeś statystyki. Wybierz z listy jedną z dostępnych statystyk.");
  }
  if (stat == "Bilety") {
    document.getElementById("statButton").href = 'ticketStats'
  }
  if (stat == "MiejscaTransakcji") {
    document.getElementById("statButton").href = 'transactionPlaceStats'
  }
  if (stat == "Transakcje") {
    document.getElementById("statButton").href = 'transactionStats'
  }
}