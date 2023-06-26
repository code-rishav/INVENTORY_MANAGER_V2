var cumTotal = 0
function addItemToTable() {
    // Get the values entered in the second form
    var itemInput = document.querySelector('input[name="item"]');
    var item = itemInput.value;
    var quantity = document.getElementById("newItemForm").elements["quantity"].value;
    var rate = document.getElementById("newItemForm").elements["rate"].value;

    // Check if any of the fields are empty
    if (item.trim() === '' || quantity.trim() === '' || rate.trim() === '') {
        alert("Please fill in all the fields.");
        return;
    }

    // Create a new row
    var newRow = document.createElement("tr");
	newRow.classList.add("item-list");

    // Create table data cells and set their values
    var itemCell = document.createElement("td");
	itemCell.classList.add("item")
    itemCell.textContent = item;

    var rateCell = document.createElement("td");
	rateCell.classList.add("rate");
    rateCell.textContent = rate;


    var quantityCell = document.createElement("td");
	quantityCell.classList.add("quantity");
    quantityCell.textContent = quantity;

    var totalCell = document.createElement("td");
	totalCell.classList.add("total")
    var total = parseFloat(rate) * parseFloat(quantity);
	cumTotal = cumTotal + total;
    totalCell.textContent = total.toFixed(2); // Adjust decimal places as needed

    // Append the cells to the new row
    newRow.appendChild(itemCell);
    newRow.appendChild(rateCell);
    newRow.appendChild(quantityCell);
    newRow.appendChild(totalCell);

    // Append the new row to the table in the first form
    var itemsTable = document.getElementById("itemsTable");
    itemsTable.appendChild(newRow);

	var cumSum = document.getElementById("totalAmount");
	cumSum.textContent = cumTotal.toFixed(2);

    // Reset the input fields of the second form
    
}

function deleteLastItemFromTable() {
	// Get the reference to the table
	var itemsTable = document.getElementById("itemsTable");
  
	// Check if there are any rows in the table
	if (itemsTable.rows.length > 1) {
	  // Remove the last row (excluding the header row)
	  var lastRowTotal = parseFloat(itemsTable.rows[itemsTable.rows.length - 1].querySelector('.total').textContent);
	  itemsTable.deleteRow(itemsTable.rows.length - 1);


	  if (itemsTable.rows.length==1)
	  cumTotal = 0;
	  else
	  cumTotal -= lastRowTotal;
  
	  // Update the cumulative total display
	  var cumSum = document.getElementById("totalAmount");
	  cumSum.textContent = cumTotal.toFixed(2);
	}
  }
function addDealer(){
	var buyer = document.querySelector('input[name="buyer"]').value;
	var holder = document.getElementById("buyer-name");
	holder.textContent = buyer;

	//this dealerData object has been parsed in the script part of html filed
	console.log(dealerData)
	for(var i=0;i<dealerData.length;i++){
		var dealerobject = dealerData[i];
		

		var name = dealerobject.pk;
		if(name==buyer){
			console.log(name);
			break;
		}
	}
	console.log(dealerobject.address,dealerobject.gstin);
	var address = document.getElementById("address");
	address.textContent = dealerobject.fields.address;
	var gstin = document.getElementById("gstin");
	gstin.textContent = dealerobject.fields.gstin;

	var currentDate = new Date();
	// Retrieve the individual components of the date
	var year = currentDate.getFullYear(); // 4-digit year (e.g., 2023)
	var month = currentDate.getMonth() + 1; // Month index starts from 0, so add 1 (e.g., 1 for January)
	var day = currentDate.getDate(); // Day of the month (e.g., 16)
	var hours = currentDate.getHours()
	var minute = currentDate.getMinutes()
	var seconds = currentDate.getSeconds()

	var formattedDate = day+"/"+month+"/"+year;

	document.getElementById("currentDate").textContent = formattedDate;

	//use the combination of date and time to create unique invoice
	var invoiceId = "P"+day+month+year+hours+minute+seconds;

	document.getElementById("invoice-id").textContent = invoiceId;
	
}

function refreshPage(){
	window.location.reload();
}

document.addEventListener('DOMContentLoaded', function() {
	// Your code here
  });

function generatePDF(){
	var element = document.getElementById('invoice-box');
	console.log(element);
	// Measure the dimensions of the HTML content
	var contentWidth = element.offsetWidth;
	var contentHeight = element.offsetHeight;
	console.log(contentWidth);
	console.log(contentHeight);
  
	// Apply CSS rule to hide the elements to be excluded
	//document.querySelectorAll(".exclude").style.display = 'none';
	var elementsToExclude = document.getElementsByClassName('exclude');
	console.log(elementsToExclude);
	for (var i = 0; i < elementsToExclude.length; i++) {
	  elementsToExclude[i].style.display = 'none';
	}
  
	/*html2pdf()
	  .set({
		margin: 8,
		filename: 'converted.pdf',
		html2canvas: { scale: 10 },
		jsPDF: { format: 'A4', orientation: 'portrait' },
		canvas: { width: contentWidth, height: contentHeight },
	  })
	  .from(element)
	  .save();*/
	  window.jsPDF = window.jspdf.jsPDF;
	  html2canvas(element).then(function (canvas) {
		var imgData = canvas.toDataURL('image/png');
		var pdf = new jsPDF('p', 'mm', 'a4');
		var pdfWidth = pdf.internal.pageSize.getWidth();
		var pdfHeight = pdf.internal.pageSize.getHeight();
		var imageWidth = canvas.width;
		var imageHeight = canvas.height;
		var scaleFactor = Math.min(pdfWidth / imageWidth, pdfHeight / imageHeight);
	
		pdf.addImage(imgData, 'PNG', 0, 0, imageWidth * scaleFactor, imageHeight * scaleFactor);
		var dealer = document.getElementById("buyer-name").textContent;
		
		var currentDate = new Date();
		// Retrieve the individual components of the date
		var year = currentDate.getFullYear(); // 4-digit year (e.g., 2023)
		var month = currentDate.getMonth() + 1; // Month index starts from 0, so add 1 (e.g., 1 for January)
		var day = currentDate.getDate(); // Day of the month (e.g., 16)

		// Format the date as desired
		var formattedDate = day + '-' + month + '-' + year;
		var fileName = dealer + "-" + formattedDate + ".pdf";
		pdf.save(fileName);

	
		// Reset the CSS rule to show the elements after conversion
		for (var i = 0; i < elementsToExclude.length; i++) {
		  elementsToExclude[i].style.display = '';
		}
	  });
	  console.log("submitted data")
	  document.getElementById("newItemForm").reset();
}
  

//to send the table data to backend
$(document).ready(function() {
	$('#generateBill').click(function() {
	  
	  var data = [];
	  console.log("called generatePDF");
	  console.log("after generatePDF");
	  
	  // Iterate over the table rows except for the header row
	  $('#itemsTable tr.item-list').each(function(index, row) {
		var rowData = {};

            // Get the values from each cell in the row
			var item = $(this).find('td.item').text().trim();
			var quantity = $(this).find('td.quantity').text().trim();
			var rate = $(this).find('td.rate').text().trim();
			var total = $(this).find('td.total').text().trim();
			console.log(item)
			console.log(rate)
			console.log(quantity)
			console.log(total)
            // Populate the rowData object

            rowData['item'] = item;
            rowData['quantity'] = quantity;
			rowData['rate'] = rate;
			rowData['total'] = total;

            // Add the rowData object to the tableData array
            data.push(rowData);
	  });

	  var buyer = document.getElementById("buyer-name").textContent;
	  var total = document.getElementById("totalAmount").textContent;
	  var invoiceid = document.getElementById("invoice-id").textContent;
	  var invoicedate = document.getElementById("currentDate").textContent;
	  

	  var requestData = {
		dealer : buyer,
		finalSum : total,
		invoiceId : invoiceid,
		invoiceDate : invoicedate,
		tabledata : data
	  };
	  


	  
	  // Send the AJAX request to the server
	  var dest = "/bill/";
	  $.ajax({
		url: dest,  // Replace with the appropriate URL mapping to your view function
		type: 'POST',
		data: JSON.stringify(requestData),
		contentType: 'application/json',
		success: function(response) {
			// Handle the successful response from the server
			// Refresh the page
			console.log("submitted");
			generatePDF();
		},
		error: function(xhr, textStatus, error) {
		  // Handle any errors that occur during the AJAX request
		  console.log(error);
		}
	  });
	  
	});
	
  });


 	