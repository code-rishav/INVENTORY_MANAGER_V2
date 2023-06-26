var pur = document.querySelector(".purchase")
var purchase = document.querySelector(".buy")
purchase.addEventListener("click",function(event){
    s.style.display = "none"
    st.style.display = "none"
    it.style.display = "none"
    dlr.style.display = "none"
    rcv.style.display = "none"
    pur.style.display = "initial";
})

var s = document.querySelector(".sale")
var sale = document.querySelector(".sold")
sale.addEventListener("click",function(event){
    pur.style.display = "none"
    st.style.display = "none"
    it.style.display = "none"
    dlr.style.display = "none"
    rcv.style.display = "none"
    s.style.display = "initial"
    
})

var st = document.querySelector(".stock")
var stock = document.querySelector(".st")
stock.addEventListener("click",function(event){
    pur.style.display = "none"
    s.style.display = "none"
    it.style.display = "none"
    dlr.style.display = "none"
    rcv.style.display = "none"
    st.style.display = "initial"
})

var it = document.querySelector(".items")
var item = document.querySelector(".it")
item.addEventListener("click",function(event){
    pur.style.display = "none"
    s.style.display = "none"
    st.style.display = "none"
    dlr.style.display = "none"
    rcv.style.display = "none"
    it.style.display = "initial"
    
})

var dlr = document.querySelector(".accounts")
var dealer = document.querySelector(".act")
dealer.addEventListener("click",function(event){
    pur.style.display = "none"
    s.style.display = "none"
    st.style.display = "none"
    it.style.display = "none"
    rcv.style.display = "none"
    dlr.style.display = "initial"
})

var rcv = document.querySelector(".recievings")
var recieving = document.querySelector(".rcv")
recieving.addEventListener("click",function(event){
    pur.style.display = "none"
    s.style.display = "none"
    st.style.display = "none"
    it.style.display = "none"
    dlr.style.display = "none"
    rcv.style.display = "initial"
})

function searchbyDate_purchase() {
    var startDateArr = [];
    var price = [];
    var sum_p = 0.0;
    var myTab = document.getElementById('tableData_p');
    let InputEndDate = document.getElementById('pdate_input2').value;
    let InputStartDate = document.getElementById('pdate_input').value;
    

    for(i = 1; i < myTab.rows.length; i++) {
        var objCells = myTab.rows.item(i).cells;
        var t1 = new Date(objCells.item(1).innerHTML)
        startDateArr.push(t1);
        var p = parseFloat(objCells.item(4).innerHTML);
        price.push(p);
    }
    var startDate = new Date(InputStartDate);
    var endDate = new Date(InputEndDate);
    startDate.setHours(0, 0, 0, 0);
    endDate.setHours(0, 0, 0, 0);
    let myTable = document.getElementById('tableData_p');
    let tr = myTable.getElementsByTagName('tr');
    if(+startDate > +endDate) {
        alert("Select Valid Date. Now please Refresh this page to continue to run code.");
    } 

    else {
        for(var j = 0; j < startDateArr.length; j++) {
            var temp1 = new Date(startDateArr[j]);
                if(+temp1 >= +startDate && +temp1 <= +endDate) {
                    tr[j + 1].style.display = "";
                    console.log(price[j+1])
                    sum_p  = sum_p+price[j]
                } else {
                    tr[j + 1].style.display = "none";
                }
        }
    }
    var get_p = document.querySelector(".price_p")
    get_p.innerHTML = "TOTAL PRICE : "+sum_p
    sum_p = 0.0
}

function searchbyDate_sale() {
    var startDateArr = [];
    var price = [];
    var sum_p = 0.0;
    var myTab = document.getElementById('tableData_s');
    let InputEndDate = document.getElementById('sdate_input2').value;
    let InputStartDate = document.getElementById('sdate_input').value;
    

    for(i = 1; i < myTab.rows.length; i++) {
        var objCells = myTab.rows.item(i).cells;
        var t1 = new Date(objCells.item(1).innerHTML)
        startDateArr.push(t1);
        var p = parseFloat(objCells.item(5).innerHTML);
        price.push(p);
    }
    var startDate = new Date(InputStartDate);
    var endDate = new Date(InputEndDate);
    startDate.setHours(0, 0, 0, 0);
    endDate.setHours(0, 0, 0, 0);
    let myTable = document.getElementById('tableData_s');
    let tr = myTable.getElementsByTagName('tr');
    if(+startDate > +endDate) {
        alert("Select Valid Date. Now please Refresh this page to continue to run code.");
    } 

    else {
        for(var j = 0; j < startDateArr.length; j++) {
            var temp1 = new Date(startDateArr[j]);
                if(+startDate <= +temp1 || +startDate === +temp1) {
                    tr[j + 1].style.display = "";
                    console.log(price[j+1])
                    sum_p  = sum_p+price[j]
                } else {
                    tr[j + 1].style.display = "none";
                }
        }
    }
    var get_p = document.querySelector(".price_s")
    get_p.innerHTML = "TOTAL PRICE : "+sum_p
    sum_p = 0.0
}

