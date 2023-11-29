from django.shortcuts import render ,HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login, logout
from ecomm_app.models import product, Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail


# Create your views here.
def about(request):
    return HttpResponse("Hello from about page")
def contact(request):
    return HttpResponse("<h1>Hello from contact page</h1>")
def edit(request,rid):
    return HttpResponse("id to be edited"+rid)
def addition(request,x1,x2):
    t=int(x1)+int(x2)
    t=str(t)
    #print("Addition is:",t)
    return HttpResponse("Addition is:"+t)
def hello(request):
    context={}
    context['greet']="Hello,we are learning DtL"
    context['x']=10
    context['y']=20
    context['l']=[10 ,20, 30, 40]
    context['products']=[
	    {'id':1,'name':'samsung','cat':'mobile','price':2000},
	    {'id':2,'name':'jeans','cat':'clothes','price':500},
	    {'id':3,'name':'vivo','cat':'mobile','price':1500},
        ]

    return render(request,'hello.html',context)
def home(request):
    #userid=request.user.id
    #print("id of logged in user:",userid)
    #print("result:",request.user.is_authenticated)
    p=product.objects.filter(is_activate=True)
    #print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)
    
def product_details(request,pid):
    p=product.objects.filter(id=pid)
    #print(p)
    context={}
    context['products']=p
    return render(request,'product_details.html',context)
def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="fields can not be empty"
            return render(request,'register.html',context)
        elif upass != ucpass:
            context['errmsg']="password & confirm password is not match"
            return render(request,'register.html',context)
        # print(uname ,upass,ucpass)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="user created successfully, Please login."
                #return HttpResponse("user created")
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="user with same name already exist"
                return render(request, 'register.html',context)
    else:
        return render(request,'register.html')
def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        print(uname,"--",upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="fields can not be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname, password=upass)
            if u is not None:
                login(request,u)#start session
                return redirect('/home')
            else:
                context['errmsg']="Invalid Username & Password"
                return render(request,'login.html',context)
            # print(u)
            #print(type(u))
            #print(u.username)
            #print(u.is_superuser)
            return HttpResponse("in else part")
        #return HttpResponse("Data fetched")
    else:
        return render(request,'login.html')
def User_logout(request):
    logout(request)
    return redirect('/home')
def catfilter(request,cv):
    print(cv)
    q1=Q(is_activate=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p 
    return render(request, 'index.html', context)
def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=product.objects.filter(is_activate=True).order_by(col)
    context={}
    context['products']=p 
    return render(request,'index.html',context)
def range(request):
    min=request.GET['min']
    max=request.GET['max']
    #print(min)
    #print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_activate=True)
    p=product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p 
    return render(request,'index.html',context)
    #return HttpResponse("value fetched")
def addtocart(request,pid):
    if request.user.is_authenticated:

        userid=request.user.id
    #print(pid)
    #print(userid)
        u=User.objects.filter(id=userid)
        #print(u[0])
        p=product.objects.filter(id=pid)
        #print(p[0])
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)

        context={}
        context['products']=p   
        if n== 1:
            context['msg']="Product Already Exist in Cart!!"
        else: 
            c=Cart.objects.create(uid=u[0], pid=p[0])
            c.save()
            context['success']="product Added Successfully"
        return render(request,'product_details.html',context)
        #return HttpResponse("product added to cart")
    else:
        return redirect('/login')

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    s=0
    np=len(c)
    #print(np)
    for x in c :
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price*x.qty
   # print(s)
    #print(c)
    #print(request.user.id)
    #print(c[0].uid)
    #print(c[0].pid)
   # print(c[0].pid.name)
    #print(c[0].pid.price)
    #print(c[0].uid.is_superuser)
    #print(c[0].pid.pdetails)
    #print(c[0].uid.username)
    context={}
    context['data']= c
    context['total']=s
    context['n']=np
    return render(request,'cart.html',context)
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')
def premove(request,sid):
    c=Order.objects.filter(id=sid)
    
    c.delete()
    return redirect('/placeorder')
def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    #print(c)
    #print(c[0])
   # print(c[0].qty)

    if qv=='1':
       t=c[0].qty+1
       c.update(qty=t)
        #pass
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
        
        #pass
    #return HttpResponse("Quantity")
    return redirect('/viewcart')
def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    #print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid, pid=x.pid, uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
        #print(x)
        #print(x.pid)
        #print(x.uid)
        #print(x.qty)
    orders=Order.objects.filter(uid=request.user.id)
    context={}
    context['data']= orders
    s=0
    np=len(orders)
    for x in orders:
        s=s+x.pid.price*x.qty
    context['total']=s
    context['n']=np
    return render(request,'placeorder.html',context)
    #return HttpResponse("in placeorder")
def makepayment(request):
    uemail=request.user.username
    #print(uemail)
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s=s+ x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_zliYLt5o06CPfz", "gWl4CrTOSqfUcKqPFjgj4JCa"))

    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    context['uemail']=uemail
    #print(payment)
    #return HttpResponse("success")
    return render(request,'pay.html',context)
def sendusermail(request,uemail):
    #print("-----------",uemail)
    
    msg="order details"
    send_mail(
        'Ekart -order placed successfully',
        msg,
        'harshada.khatavkar0@gmail.com',
        [uemail],
        fail_silently=False,
    )
    return HttpResponse("mail send successfully")