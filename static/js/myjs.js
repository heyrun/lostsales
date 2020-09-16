$(function () {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function get_item(item) {
    const csrftoken = getCookie("csrftoken");

    $.ajax({
      headers: { "X-CSRFToken": csrftoken },
      url: "additem",
      type: "POST",
      data: { id: item, TEST: "test" },
      success: function (data) {
        console.log(data["upc"]);
        $("#modelId").modal({
          fadeDuration: 500,
          fadeDelay: 0.5,
        });
        document.getElementById("upc").innerHTML = data["upc"];
        document.getElementById("description").innerHTML = data["description"];
        document.getElementById("attributes").innerHTML = data["attributes"];
        document.getElementById("size").innerHTML = data["size"];
        // document.getElementById("product").val = item;
        document.getElementById("product").value = data["id"];
        return false;
      },
      error: function () {
        $("#results").html(
          "<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " +
            errmsg +
            " <a href='#' class='close'>&times;</a></div>"
        ); // add the error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      },
    });
  }

  $(".save").click(function (e) {
    e.preventDefault();
    var item = $(this).prop("value");

    get_item(item);
  });

  $(".upc").autocomplete({
    source: "{% url 'additem' %}" /*used to be allcaptures */,
    minLength: 4,
  });

  function create_post() {
    const csrftoken = getCookie("csrftoken");

    $.ajax({
      headers: { "X-CSRFToken": csrftoken },
      url: "captureloss",
      type: "POST",
      data: { product: $("#product").val() },
      success: function (json) {
        console.log("successfully sent");
      },
      error: function () {
        $("#results").html(
          "<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " +
            errmsg +
            " <a href='#' class='close'>&times;</a></div>"
        ); // add the error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      },
    });
  }

  $("#contactForm").submit(function (event) {
    event.preventDefault();
    console.log("form submitted!");

    create_post();
  });
});

//script for form submission
