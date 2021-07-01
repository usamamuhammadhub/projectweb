
from os import name
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from app.models import About_us, Services,Customer,OrderPlaced


from PIL import Image
from django import forms
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import to_language
from django.views import View
from .models import Cart, Customer,  OrderPlaced
from .forms import CustomerRegistrationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomerForm,Orderfrom,Servicesform





class ServiceView(View):
 def get(self ,request):
  as_perr = Services.objects.filter(as_per='Day')

  # bottomwers = Services.objects.filter(as_per='BW')
  # mobiles =Services.objects.filter(category='M')
  fott =Services.objects.filter(as_per='Square Fit')
  return render(request, 'app/home.html', {'as_perr': as_perr, 'fott': fott})


# sevice show
def sevice(request, data=None):
    if data == None:
        sevices = Services.objects.all()

    # elif data=='toyota' or data=='dk':
    #      mobiles=Product.objects.filter(category='M').filter(Brand=data)

    return render(request, 'app/services.html', {'sevices': sevices})


# About us
def about(request):
    ab = About_us.objects.all()

    return render(request, 'app/about.html', {'ab': ab})






 # About us
def abouts(request):
    ab = About_us.objects.all()

    return render(request, 'app/abouts.html', {'ab': ab})   


# customerrigtation

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.info(request, 'Congratulations You are Register')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


# login funtion
# def login1(request):
#   return render(request, 'app/login.html')


# after login redirct
@login_required
def dash(request):
    return render(request, "app/dashbase.html")


# view services in customer dash board
@login_required
def viewserviescustomerdash(request, data=None):
    if data == None:
        services = Services.objects.all()
    elif data == 'Billboard' or data == 'Creatives' or data == 'Streamers':
        services = Services.objects.filter(title=data)

    return render(request, 'app/dashservices.html', {'services': services})


# def viewserviescustomerdash(request,data=None):
# if data== None:
# services=Services.objects.all()


# return render(request,'app/dashservices.html',{'services': services})

# class viewserviescustomerdash(View):
# def get(self,request,pk):
#  services=Services.objects.get(pk=pk )
# item_already_in_cart=False
# item_already_in_cart =Cart.objects.filter(Q(service=service.id)& Q(user=request.user)).exists()

# return render(request,'app/servicedetail.html',{'services':services})


def index(request):
    return render(request, "app/index.html")


def inner_page(request):
    #  params= {'name':'usama','place':'okara'}
    return render(request, "app/inner-page.html")


def portfolio_details(request):
    return render(request, "app/portfolio-details.html")


# def home(request):

# return render(request,"app/home.html")


# def bas(request):

#   return render(request,"app/base1.html")
# @method_decorator(login_required,name='dispatch')
@method_decorator(login_required,name='dispatch')
class service_detail(View):
    def get(self, request, pk):
        service = Services.objects.get(pk=pk)
        item_already_in_cart=False
        item_already_in_cart =Cart.objects.filter(Q(service=service.id)& Q(user=request.user)).exists()

        #return render(request, 'app/servicedetail.html', {'servic': servic})
        return render(request,'app/servicedetail.html',{'service':service,'item_already_in_cart':item_already_in_cart})


# add to card
@login_required
def add_to_cart(request):
    user = request.user
    service_id = request.GET.get('ser_id')
    service = Services.objects.get(id=service_id)
    Cart(user=user, service=service).save()
    return redirect('showcart')

@login_required
def showcart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0
        cart_service = [p for p in Cart.objects.all() if p.user == user]
        if cart_service:
            for p in cart_service:
                tempamount = (p.quantity * p.service.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount

            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount})
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        ser_id = request.GET['ser_id']
        c = Cart.objects.get(Q(service=ser_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 0.0
        cart_service = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_service:
            tempamount = (p.quantity * p.service.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount

        data = {'quantity': c.quantity, 'amount': amount, 'totalamount': totalamount}
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        ser_id = request.GET['ser_id']
        c = Cart.objects.get(Q(service=ser_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 0.0
        cart_service = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_service:
            tempamount = (p.quantity * p.service.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount

        data = {'quantity': c.quantity, 'amount': amount, 'totalamount': totalamount}
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        ser_id = request.GET['ser_id']
        c = Cart.objects.get(Q(service=ser_id) & Q(user=request.user))

        c.delete()
        amount = 0.0
        shipping_amount = 0.0
        cart_service = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_service:
            tempamount = (p.quantity * p.service.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount

        data = {'amount': amount, 'totalamount': totalamount}
        return JsonResponse(data)


"""
def about(request):
    return HttpResponse("about")
     """

# def openbutten(request):
# return HttpResponse('''<a href="https://www.youtube.com/" >open </a>''')
"""
def remove(request):
    page = request.GET.get('text','default')
    print(page)
    #text analzsis



    return HttpResponse("remove punctionation")
    """


def home(request):
    return render(request, 'app/home.html')





#

@login_required
def checkout(request):
   user=request.user
   add=Customer.objects.filter(user=user)
   cart_item = Cart.objects.filter(user=user)
   amount=0.0
   shipping_amount =0.0
   totalamount=0.0
   cart_service= [p for p in Cart.objects.all() if p.user==request.user]
   if cart_service:
      for p in cart_service:
         tempamount=(p.quantity*p.service.discounted_price)
         amount+=tempamount
      totalamount= amount+shipping_amount
      return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_item':cart_item})



@login_required
def pymentdone(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    if customer:
      cart=Cart.objects.filter(user=user)
      messag='none'
      for c in cart:
        OrderPlaced(user=user,customer=customer,service=c.service,quantity=c.quantity,message=messag).save()
        c.delete()
    else:
        return redirect('CustomerFormview/')    
    return redirect("orders")

@login_required
def orders(request):
   ordplc=OrderPlaced.objects.filter(user=request.user)
   
   return render(request, 'app/orders.html',{'ordplc':ordplc})










#add to order
"""
def add_to_order(request):
    user = request.user
    service_id = request.GET.get('ser_id')
    service = Services.objects.get(id=service_id)
    if request.method=='POST':
        start_date=request.POST.get('stdate')
        end_date=request.POST.get('enddate')
        messag=request.POST.get('msg')


        OrderPlaced(user=user, service=service,customer=user,start_date=start_date,end_date=end_date,message=messag).save()
        messages.success(request,'date enter')
    return redirect(request,'orders.html')"""



#customerprofile
@login_required
def CustomerFormview(request):
    user=request.user
    if request.method == 'POST':
        fm=CustomerForm(request.POST, request.FILES)
        if fm.is_valid():
            
            name=fm.cleaned_data['name']
            email=fm.cleaned_data['email']
            phon=fm.cleaned_data['phone_no']
            whattpp=fm.cleaned_data['whatsapp_no']
            mobile=fm.cleaned_data['mobile']
            state=fm.cleaned_data['state']
            country=fm.cleaned_data['country']
            city=fm.cleaned_data['city']
            Address=fm.cleaned_data['Address']
            image=fm.cleaned_data['customer_image1']
            Customer(user=user,name=name,email=email,whatsapp_no=whattpp,phone_no=phon,mobile=mobile,country=country,state=state,city=city,Address=Address,customer_image1=image).save()
            return redirect('viewcustomeredit')            

    else:
        fm=CustomerForm()
    return render(request,'app/cutomerprofileform.html',{'form':fm})        


#fectch the customer detail
@login_required
def viewcustomeredit(request):
    
    customer = Customer.objects.all()


    return render(request, 'app/customerviewupdate.html', {'form':  customer})

#deting custumen detail
def delcustomeredit(request,id):
    if request.method=='POST':
        pi=Customer.objects.get(pk=id)
        pi.delete()
        return redirect('delcustomeredit/')



#update custumen detail
@login_required
def updatecustomeredit(request,id):
    if request.method=='POST':
        pi=Customer.objects.get(pk=id)
        
        fm=CustomerForm(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
            return redirect('viewcustomeredit')      
        

    else:
          pi=Customer.objects.get(pk=id)
        
          fm=CustomerForm(instance=pi)  
    return render(request,'app/update.html',{'form':fm })



#order delete

def delorder(request,id):
    if request.method=='POST':
        pi=OrderPlaced.objects.get(pk=id)
        pi.delete()
        return redirect('orders')      




# order update
def updateorder(request,id):

    if request.method=='POST':
        pi=OrderPlaced.objects.get(pk=id)
        
        fm=Orderfrom(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
            return redirect('orders')      
        

    else:
          pi=OrderPlaced.objects.get(pk=id)
        
          fm=Orderfrom(instance=pi)  
    return render(request,'app/orderupdate.html',{'form':fm })














#add services
def addservices(request):
    user=request.user
    if request.method == 'POST':
        fm=Servicesform(request.POST, request.FILES)
        if fm.is_valid():
            title=fm.cleaned_data['title']
            Actual_price=fm.cleaned_data['Actual_price']
            discounted_price=fm.cleaned_data['discounted_price']
            as_per=fm.cleaned_data['as_per']
            description=fm.cleaned_data['description']
            Service_image1=fm.cleaned_data['Service_image1']
            Service_image2=fm.cleaned_data['Service_image2']
            Services(title=title,Actual_price=Actual_price,discounted_price=discounted_price,as_per=as_per,description=description,Service_image1=Service_image1,Service_image2=Service_image2).save()
            return redirect('viewserviescustomerdash')            

    else:
        fm=Servicesform()
    return render(request,'app/seviceadd.html',{'form':fm}) 

