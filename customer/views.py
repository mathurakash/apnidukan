from unicodedata import category
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from ecom.models import Product,Category, SubCategory
from django.views import generic
from django.contrib.auth.models import User
from .forms import  CReg,Clog
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import razorpay
from .models import Payment
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

'''def home(request):
    c=Category.objects.all()
    return render(request,"customer/home.html",{'cat':c})
'''


# class Home(generic.ListView):
#     def get(self,request):
#         template_name="customer/home.html"
#         context_object_name='cat'
#         def get_queryset(self):
#             return Category.objects.all()

#     def post(self,request):
#            product=request.POST.get('productid')
#            print(product)
           
class Home(generic.ListView):
    template_name="customer/home.html"
    context_object_name='cat'
    model=Category

def AddToCart(request,pk):
    product=request.POST.get('productid')
    cart=request.session.get('cart')
    if cart:
        quantity=cart.get(product)
        if quantity:
            cart['product']=quantity+1
        else:
            cart['product']=1
    else:
        cart={}
        cart['product']=1
    request.session['cart']=cart
    print(product)
    print(request.session['cart'])
    return redirect('customer:home')
    #     song = Song.objects.get(id=pk)
    # song.likes += 1
    # song.save()
    # return redirect('music:home')


class Register(generic.View):
    def get(self,request):
        return render(request,"customer/form.html",{'form':CReg(None)})
    def post(self,request):
        f=CReg(request.POST)
        if f.is_valid():
            data=f.save(commit=False)
            p=f.cleaned_data.get("password")
            data.set_password(p)
            # data.is_superuser=True
            data.save()
            return redirect("customer:c-signin")
        return render(request,"customer/form.html",{'form':f})



class LoginPage(generic.View):
    def get(self,request):
        return render(request,"customer/form.html",{'form':Clog(None)})
    def post(self,request):
        f=Clog(request.POST)
        if f.is_valid():
            u=f.cleaned_data.get("username")
            p=f.cleaned_data.get("password")
            cat=Category.objects.all()
            usr=authenticate(username=u,password=p)
            nxt=request.GET.get('next')
            if usr:
                login(request,usr)
            if nxt:
                return redirect(nxt)
            return redirect("customer:main")
        return render(request,"customer/form.html",{'form':f})


def signout(request):
    logout(request)
    return redirect("customer:main")


class Detailpage(generic.DetailView):
    template_name="customer/home.html"
    model=SubCategory
    context_object_name='sub'
    def get_context_data(self, **kwargs):
        data=super().get_context_data(**kwargs)
        data['cat']=Category.objects.all()
        return data

class Productpage(generic.DetailView):
    template_name="customer/detail.html"
    model=Product
    context_object_name='prod'

class Buy(LoginRequiredMixin,generic.DetailView):
    login_url='customer:c-signin'
    template_name="customer/buy.html"
    model=Product
    context_object_name='prod'





def pay(request):
    if request.method=='POST':
        name = request.POST.get("name")
        amount = int(request.POST.get("amount")) * 100 # I wrote amount variable in lowercase
        print(name,amount)
        client = razorpay.Client(auth=("rzp_test_JkLhsObiDUT936","ydlBTS3AGmpuehr8pY5XkTRy"))
        payment = client.order.create({'amount':amount, 'currency':'INR','payment_capture':'1'})
        print("----------------------------")
        print(name,amount,client,payment)
        coffee=Payment(name=name,amount=amount,payment_id=payment['id'])#In this also i used lowercase for variables.
        coffee.save( )
        # return render(request,'pay.html',{'payment':payment,'name':name})
        return render(request,"customer/buy.html")        
    return render(request,"customer/buy.html") 


@csrf_exempt
def success(request):
    if request.method == 'GET':
        name = request.POST.get("name")
        amount = int(request.POST.get('amount'))*100 # I wrote amount variable in lowercase
        client = razorpay.Client(auth=("rzp_test_JkLhsObiDUT936","ydlBTS3AGmpuehr8pY5XkTRy"))
        payment = client.order.create({'amount':amount, 'currency':'INR','payment_capture':'1'})
        coffee=Payment(name=name,amount=amount,payment_id=payment['id'],paid=True)#In this also i used lowercase for variables.
        coffee.save( )
        return render(request,"success.html")
    else:
        return render(request,"customer/buy.html") 




