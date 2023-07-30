var purchase = document.getElementById("showPurchase");
var sale = document.getElementById("showSale");

var pur = document.getElementById("purchase-data")
var sal = document.getElementById('sale-data');



purchase.addEventListener('click',function(){
    pur.style.display = 'initial';
    sal.style.display = 'none';
})

sale.addEventListener('click',function(){
    pur.style.display = 'none';
    sal.style.display = 'initial';
})