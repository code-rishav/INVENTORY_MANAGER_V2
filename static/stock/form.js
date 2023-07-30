function addItemToTable() {
    // Get the values entered in the second form
    var itemInput = document.querySelector('input[name="item"]');
    var item = itemInput.value;
    console.log(item)
    var quantity = document.getElementById("newItemForm").elements["quantity"].value;
    var rate = document.getElementById("newItemForm").elements["rate"].value;

    if (item.trim() === '' || quantity.trim() === '' || rate.trim() === '') {
        alert("Please fill in all the fields.");
        return;
    }

    // Create a new row
    var newRow = document.createElement("tr");

    // Create table data cells and set their values
    var itemCell = document.createElement("td");
    itemCell.innerHTML = '<input type="text" name="item[]" value="your_item_value"> item';
    
    /*var iteminput = document.createElement("input");
    iteminput.setAttribute("type","text");
    iteminput.setAttribute("name","item[]");
    itemCell.appendChild(iteminput);
    var textNode = document.createTextNode(item); // Create a text node with the desired content
    itemCell.appendChild(textNode);*/


    var rateCell = document.createElement("td");
    var rateinput = document.createElement("input");
    rateinput.setAttribute("type","number");
    rateinput.setAttribute("name","rate[]");
    rateCell.appendChild(rateinput);
    rateCell.textContent = rate;
    

    var quantityCell = document.createElement("td");
    var quantityinput = document.createElement("input");
    quantityinput.setAttribute("type","text");
    quantityinput.setAttribute("name","item[]");
    quantityCell.appendChild(quantityinput);
    quantityCell.textContent = quantity;

    var totalCell = document.createElement("td");
    var total = parseFloat(rate) * parseFloat(quantity);
    var totalinput = document.createElement("input");
    totalinput.setAttribute("type","text");
    totalinput.setAttribute("name","item[]");
    totalCell.appendChild(totalinput);
    
    totalCell.textContent = total.toFixed(2); // Adjust decimal places as needed

    // Append the cells to the new row
    newRow.appendChild(itemCell);
    newRow.appendChild(rateCell);
    newRow.appendChild(quantityCell);
    newRow.appendChild(totalCell);

    // Append the new row to the table in the first form
    var itemsTable = document.getElementById("itemsTable");
    itemsTable.appendChild(newRow);

    // Reset the input fields of the second form
    document.getElementById("newItemForm").reset();
}

function addItemTable(){
    var newRow = document.createElement("tr");

    var itemCell = document.createElement("td");
    var iteminput = document.createElement("input");
    iteminput.setAttribute("type","text");
    iteminput.setAttribute("name","item[]");
    itemCell.appendChild(iteminput);
    

    var rateCell = document.createElement("td");
    var rateinput = document.createElement("input");
    rateinput.setAttribute("type","number");
    rateinput.setAttribute("name","rate[]");
    rateCell.appendChild(rateinput);

    var quantityCell = document.createElement("td");
    var quantityinput = document.createElement("input");
    quantityinput.setAttribute("type","text");
    quantityinput.setAttribute("name","item[]");
    quantityCell.appendChild(quantityinput);

    var totalCell = document.createElement("td");
    var total = parseFloat(rate) * parseFloat(quantity);
    var totalinput = document.createElement("input");
    totalinput.setAttribute("type","text");
    totalinput.setAttribute("name","item[]");
    totalCell.appendChild(totalinput);

    newRow.appendChild(itemCell);
    newRow.appendChild(rateCell);
    newRow.appendChild(quantityCell);
    newRow.appendChild(totalCell);

    var itemsTable = document.getElementById("itemsTable");
    itemsTable.appendChild(newRow);

}

  var src = '/entryF/'
  $.ajax({
    url: src,
    type: 'GET',
    success: function(response) {
      if (response.error) {
        // Display the error message in the alert container
        alert(response.error);
      }
    },
    error: function(xhr, textStatus, errorThrown) {
      // Handle any errors that occur during the AJAX request
      console.log(errorThrown);
    }
  });
    
