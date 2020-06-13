//Zapisanie miejsca transakcji w przeglądarce
function setPlace() {
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
  
function setTicketType(d){
    var type = new Object();
    type.value = d
    window.localStorage.setItem("type", JSON.stringify(type));
}

function setReduction(r){
    var reduction = new Object();
    reduction.value = r
    window.localStorage.setItem("reduction", JSON.stringify(reduction));
}

function pay(id){
    const data = {
        payment : id,
        place : JSON.parse(window.localStorage.getItem('place')).id,
        reduction: JSON.parse(window.localStorage.getItem('reduction')).value,
        type: JSON.parse(window.localStorage.getItem('type')).value
    }
    console.log(id,data)
    sendTransactionRequest(data, function(response) { // success
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
function sendOrderError(xhr, textstatus) {
    alert("BŁĄD");
  }