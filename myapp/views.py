from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Product,Cart,Order
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
import random
import razorpay

# Create your views here.

def com(request):
    context={}
    p=Product.objects.all()
    context['products']=p
    print(p)
    print(request.user.id)
    print(request.user.is_authenticated)
    return render(request,"index.html",context)

def register(request):
    context={}
    if request.method=="POST":
        un=request.POST["uname"]
        un1=request.POST["password"]
        un2=request.POST["cpassword"]
        
        if un=="" or un1=="" or un2=="":
            context["errmsg"]="Fields cannot be empty"
            return render(request,"register.html",context)
        elif un1 !=un2:
            context["errmsg"]="password and cpassword didnt match"  
            return render(request,"register.html",context) 
        else:
            u=User.objects.create(username=un,email=un2)
            u.set_password(un1)
            u.save()
            context["success"]="Registration successful!!"
            return render(request,"register.html",context)
    else:
        return render(request,"register.html")
             
def ulogin(request):
    context={}
    if request.method=="POST":
        
        un=request.POST["uname"]
        un1=request.POST["password"] 
        print(un,un1)
        u=authenticate(username=un,password=un1)
        print(u)  
        
        if u is not None:
            login(request,u)
            #return redirect("/index")
            return redirect(request,"login.html",context) 
        else:
            context["errmsg"]="Invalid username and password"
            return render(request,"login.html",context) 
                 
    return render(request,"login.html")

def ulogout(request):
    logout(request)
    return redirect('/index')

def catfilter(request,cv):
    p=Product.objects.filter(cat=cv)
    context={}
    context["products"]=p
    return render(request,"index.html",context)

def sort(request,pv):
    context={}
    if pv=="0":
        p=Product.objects.order_by("-price").filter(is_active=True)
    else:
        p=Product.objects.order_by("price").filter(is_active=True)
    context['products']=p
    return render(request,"index.html",context)

def filterbyprice(request):
    mn=request.GET["min"]
    mx=request.GET["max"]
    
    q1=Q(price__gte=mn)
    q2=Q(price__lte=mx)
    p=Product.objects.filter(q1&q2)
    context={"products":p}
    return render(request,"index.html",context)

def productdetails(request,rid):
    print(rid)
    p=Product.objects.filter(id=rid)
    context={}
    context['products']=p  
    return render(request,"productdetails.html",context)
    
   
def viewcart(request):
    context={}  
    c=Cart.objects.filter(userid=request.user.id)
   #C
    q1=c[0].qty
    context["carts"]=c
    sum=0
    for x in c:
        sum=sum+x.pid.price*x.qty
        
    print(sum)
    context["total"]=sum
    context["items"]=len(c)
    
        
        
    return render(request,"cart.html",context)


def addtocart(request,pid):
    #print(pid)
    context={}
    
    if request.user.is_authenticated:
        
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        context["data"]=p
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        if n==1:
            context["msg"]="Product already Exist in cart"
            return render(request,"productdetails.html",context)
        else:
             c=Cart.objects.create(pid=p[0],userid=u[0])
             c.save()
             context["msg"]="Product added in cart successfully" 
             
             return render(request,"productdetails.html",context)
        
    else:
        return redirect('/ulogin')
    
    
def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    print(q)
    if x=="1":
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    
    return redirect("/viewcart")


def placeorder(request):
    c=Cart.objects.filter(userid=request.user.id)
    orderid=random.randrange(1000,9999)
    for x in c:
        amount=x.qty* x.pid.price
        o=Order.objects.create(order_id=orderid,amt=amount,p_id=x.pid,user_id=x.userid)
        o.save()
        x.delete()
    
    return redirect("/fetchorder")


def fetchorder(request):
    orders=Order.objects.filter(user_id=request.user.id)
    context={}
    context["orders"]=orders
    sum=0
    for x in orders:
        sum=sum+x.amt
    context["totalamount"]=sum
    context['n']=len(orders)
    return render(request,"placeorder.html")


def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_xH25KVBomhTNdB", "GsB4Ok8KwgMglbd1o9MaCnJR"))
    orders=Order.objects.filter(user_id=request.user.id)
    context={}
    context["orders"]=orders
    sum=0
    
    for x in orders:
        sum=sum+x.amt 
        orderid=x.order_id
        
    data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context["payments"]=payment
    return render(request,"pay.html")
