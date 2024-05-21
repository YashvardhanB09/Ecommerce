from django.db import models

# Create your models here.

class Product(models.Model):
    CAT=((1,"shoes"),(2,"electronic"),(3,"cloths"),(4,"Education"),(5,"Fashion"))
    SORT=((0,"hightolow"),(1,"lowtohigh"),(2,"newestarrival"),(3,"avgreview"))
    name=models.CharField(max_length=20,verbose_name="product Name")
    price=models.IntegerField()
    cat=models.IntegerField(choices=CAT,verbose_name="Catagory")
    Pdetails=models.CharField(max_length=200, verbose_name="Details")
    is_active=models.BooleanField(default=True, verbose_name="Is_Available")
    pimage=models.ImageField(upload_to="image")
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    userid=models.ForeignKey('auth.User',on_delete=models.CASCADE, db_column='userid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    
#C   
class Order(models.Model):
    order_id=models.CharField(max_length=50)
    user_id=models.ForeignKey('auth.User',on_delete=models.CASCADE, db_column='userid')
    p_id=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    amt=models.FloatField()
    

 

