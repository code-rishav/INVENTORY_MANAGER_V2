from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100,primary_key=True,default='')
    packet = models.IntegerField(default=0)
    slug = models.SlugField(blank=True,default='item')
    mrp = models.DecimalField(max_digits=6,decimal_places=2)
    invoice_rate = models.DecimalField(max_digits=9,decimal_places=2,default=0)

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        slug = slugify(self.name)
        return super().save(*args, **kwargs)
        
    
    def get_absolute_url(self):
        return reverse('item', args=(str(self.id),))


class Purchase(models.Model):
    item = models.ForeignKey(Item,on_delete=models.PROTECT,default='')
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=9,decimal_places=2) 
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Item name: {self.item}"
    
class Dealer(models.Model):
    name = models.CharField(max_length=60,primary_key=True,default='')
    gstin = models.CharField(max_length=30,default='')
    balance = models.DecimalField(max_digits=9,decimal_places=2,default=0.0,blank=True)
    address = models.CharField(max_length=70,default='')
    slug = models.SlugField()

    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):

        self.slug = slugify(self.name)
        return super().save(*args,**kwargs)



class Account(models.Model):
    name = models.ForeignKey(Dealer,on_delete=models.PROTECT,default='')
    lend_amt = models.IntegerField(default=0)
    rcv_amt = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name


    
class Sale(models.Model):
    item = models.ForeignKey(Item,on_delete=models.PROTECT,default='')
    quantity = models.IntegerField(default=0)
    rate = models.DecimalField(max_digits=9,decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    dealer = models.ForeignKey(Dealer,on_delete=models.PROTECT,default='')
    amount = models.DecimalField(max_digits=9,decimal_places=2,default=0)
    

    def __str__(self):
        return self.item.name +" - " + self.dealer.name
    
    def save(self,*args,**kwargs):
        self.amount = self.quantity * self.rate
        return super().save(*args, **kwargs)
    

class Stock(models.Model):
    item = models.ForeignKey(Item,on_delete=models.PROTECT)
    quantity = models.IntegerField(null=0,blank=True)

    def __str__(self):
        return self.item.name
    
class Invoice(models.Model):
    invoiceId = models.CharField(max_length=20,default='')
    dealer = models.ForeignKey(Dealer,on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=9,decimal_places=2)

    def __str__(self):
        return self.dealer.name +"-"+ str(self.date)
    
class Recieving(models.Model):
    dealer = models.ForeignKey(Dealer,on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=9,decimal_places=2)

    #create text choice for type of receiving
    rcv_choice = [
        ('BORROW',_('B')),
        ('PAID',_('P')),
    ]
    type = models.CharField(max_length=6,choices=rcv_choice)
    balance = models.DecimalField(max_digits=9,decimal_places=2)


    def __str__(self):
        return self.dealer.name +"-"+ str(self.date)
