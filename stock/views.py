from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout 
from django.utils.html import format_html
import json
from django.db.models import Sum, Count
from json import dumps
from django.core import serializers
from django.contrib import messages
from django.db import transaction

from stock.models import * 
from django.http import HttpResponseRedirect,JsonResponse
from django.template.loader import render_to_string
from django.template.loader import get_template
# Create your views here.
def dealer(request,slug=None):
    dealer = Dealer.objects.get(slug=slug)
    recieving = reversed(Recieving.objects.filter(dealer=dealer))
    return render(request,'stock/dealer.html',{'recievings':recieving,'dealer':dealer})

def items(request,name=None):
    item = Item.objects.get(name=name)
    if request.method == "GET":
        purchase = Purchase.objects.filter(item=item)
        sale = Sale.objects.filter(item=item)
        print("in get request")
    
    if request.method == "POST":
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        purchase = Purchase.objects.filter(
            item=item,
            date__range = [startDate,endDate]
            )
        sale = Sale.objects.filter(
            item=item,
            date__range=[startDate,endDate]
        )
        print("recieved the date",startDate," ",endDate)

    #purchase data 
    pamt = purchase.aggregate(total_amount=Sum('amount'))['total_amount']
    pqty = purchase.aggregate(total_quantity=Sum('quantity'))['total_quantity']


    #sale data 
    samt = sale.aggregate(total_amount=Sum('amount'))['total_amount']
    sqty = sale.aggregate(total_quantity=Sum('quantity'))['total_quantity']

    context = {
        'item':item,
        'purchase': purchase,
        'pqty':pqty,
        'pamt':pamt,
        'sale':sale,
        'samt':samt,
        'sqty':sqty
    }

    return render(request, 'stock/item-detail.html', context)








def homepage(request):
    items = Item.objects.all()
    purchase = reversed(Purchase.objects.all())
    sale = reversed(Sale.objects.all())
    stock = Stock.objects.order_by('-quantity')
    dealers = Dealer.objects.order_by('name')
    recievings = Recieving.objects.all()
    context = {'items':items,'purchase':purchase,'sale':sale,'stock':stock,'dealers':dealers,'recievings':recievings}
    return render(request,'stock/stocks.html',context)

def logout_view(request):
    logout(request)
    return redirect('login')

def detail(request,id=None):
    purchase = get_object_or_404(Purchase,id=id)
    return render(request,'stock/detail.html',{'purchase':purchase})




@transaction.atomic
def entryForm(request):

    all_items = Item.objects.all()
    if request.method=="POST":
        if request.POST.get("newItem"):
            item = request.POST.dict()
            name = item.get("itemname")
            packets = item.get("packets")
            mrp = item.get("mrp")
            invoiceRate = item.get("invoice-rate")

            try:
                with transaction.atomic():
                    newItem = Item(name=name,packet=packets,mrp=mrp,invoice_rate=invoiceRate)
                    newItem.save()
                    #add this item to stock table
                    newStock = Stock(item=newItem,quantity=0)
                    newStock.save()
            except Exception as e:
                transaction.set_rollback(True)
                error = "There was an error in while submitting, please enter again"
                return JsonResponse(error,safe=False)

        elif request.POST.get("newPurchase"):
            

            try:
                purchase = request.POST.dict()
                itemname = purchase.get("item")
                item  = Item.objects.get(name=itemname)
                quantity = purchase.get("quantity")
                date = purchase.get("date")
                amount = float(quantity) * float(item.invoice_rate)
                with transaction.atomic():
                    newPurchase = Purchase(item=item,quantity=quantity,date=date,amount=amount)
                    newPurchase.save()
            except Exception as e:
                print("error",e)
                transaction.set_rollback(True)
                error = "There was an error in while submitting, please enter again"
                return JsonResponse(error,safe=False)
                #return render(request,'stock/sale-form.html',{'items':all_items})

            
        
        elif request.POST.get("newDealer"):
            try:
                with transaction.atomic():
                    dealer = request.POST.dict()
                    dealer_name  = dealer.get("dealername")
                    gstin = dealer.get("gstin")
                    address = dealer.get("address")
                    dealerobj = Dealer(name=dealer_name,gstin=gstin,address=address)
                    dealerobj.save()
            except Exception as e:
                transaction.set_rollback(True)
                error = "There was an error in while submitting, please enter again"
                return JsonResponse(error,safe=False)

            
    
    return render(request,'stock/sale-form.html',{'items':all_items})

@transaction.atomic
def generateBill(request):
    items = Item.objects.all()
    #retrieve all necessary data to send to the html page
    buyer = Dealer.objects.all()
    buyer_json = serializers.serialize('json',  buyer)


    if request.method=="POST":
        try:
            with transaction.atomic():

                data = json.loads(request.body)

                #generate invoice data and add it to database
                dealername = data.get('dealer')
                totalSum = data.get('finalSum')
                invoiceId = data.get('invoiceId')
                invoiceDate = data.get('invoiceDate')

                #get teh table data
                table_data =  data.get('tabledata',[])

                #update dealer data
                dealer = Dealer.objects.get(name=dealername)
                dealer.balance = float(dealer.balance) + float(totalSum)
                
                
                for row in table_data:
                    updateTables(row,dealer,invoiceDate)
                
                
                

                invoice = Invoice(invoiceId=invoiceId,date=invoiceDate,dealer=dealer,amount=totalSum)
                

                #insert new data to recieving table
                recieving = Recieving(dealer=dealer,date=invoiceDate,amount=float(totalSum),balance=dealer.balance,type='BORROW')
                recieving.save()
                invoice.save()
                dealer.save()
        except Exception as e:
            print(e)
            transaction.set_rollback(True)
            error = "An error occured while submitting the bill, please enter again"
            return JsonResponse( error,safe=False)
            
                
            
        return render(request,'stock/bill-template.html',{'items':items,'dealer':dealer})
        

    return render(request,'stock/bill-template.html',{'buyer':buyer,'items':items,'buyer_json':buyer_json})
    

@transaction.atomic
def updateTables(row,dealer,invoiceDate):
    try:
        with transaction.atomic():

            name = row['item']
            rate = float(row['rate'])
            quantity = int(row['quantity'])
            total = float(row['total'])

            item = Item(name=name)
            itemS = Stock.objects.get(item=item)
            itemS.quantity = itemS.quantity - int(quantity)
            if(itemS.quantity<0):
                messages.error(item.name,"is not enough in stock, please check stock")
                raise Exception("negative stock")
            

            #create sale entry
            sale = Sale(item=item,quantity=quantity,date=invoiceDate,rate=rate,dealer=dealer,amount=total)
            sale.save()

            
            return total
    except Exception as e:
        error = "There was an error in while submitting, please enter again"
        return JsonResponse(error,safe=False)

def createBill(request):
    item = Item.objects.all()

    return render(request,'stock/bill-template.html',{'items':item})


@transaction.atomic
def updateAccounts(request):
    try:
        with transaction.atomic():

            dealers = Dealer.objects.all()
            if request.method == "POST":
                data = request.POST.dict()
                name = data.get("dealer")
                date = data.get("date")
                amount = float(data.get("amount"))

                dealer = Dealer(name=name)

                #update the balance amount 
                updateDealer = Dealer.objects.get(name=dealer.name)
                updateDealer.balance = float(updateDealer.balance) - (amount)
                updateDealer.save()
                
                recieving = Recieving(dealer=dealer,date=date,amount=amount,balance=updateDealer.balance,type='PAID')
                recieving.save()
    except Exception as e:
        transaction.set_rollback(True)
        error = "There was an error in while submitting, please enter again"
        return JsonResponse(error,safe=False)



    return render(request,'stock/accounts-update.html',{'dealers':dealers})
