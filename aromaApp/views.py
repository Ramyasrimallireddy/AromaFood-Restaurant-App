from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Cart, User, Restuarant, Items
import razorpay
from django.conf import settings

# Create your views here.
def index(request):
    return render(request,'index.html')
def open_signup(request):
    return render(request,'signup.html')
def open_signin(request):
    return render(request,'signin.html')
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        if User.objects.filter(email = email).exists():
            return HttpResponse("User already exists with this email")
        if User.objects.filter(phone = phone).exists():
            return HttpResponse("User already exists with this phone number")

        user = User(username = username,phone = phone,email=email,password = password,address = address)
        user.save()
        return render(request, 'signin.html', {'message': 'Signup successful!'})
    else:
        return HttpResponse("Invalid Response")
def signin(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            User.objects.get(username = username,password = password)
            if username == "admin":
                return render(request,'admin_home.html')
            else:
                restuarants = Restuarant.objects.all()
                return render(request,'customer_home.html',{'restuarants':restuarants,'username':username})
        except User.DoesNotExist:
            return render(request,'fail.html')
def open_add_restuarant(request):
    return render(request,'add_restuarant.html')

def add_restuarant(request):
    if request.method == 'POST':
        restuarant_name = request.POST.get('restuarant_name')
        location = request.POST.get('location')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        picture = request.POST.get('picture')
        try:
            Restuarant.objects.get(restuarant_name = restuarant_name)
            return HttpResponse("Duplicate restaurant!")
        except :
            Restuarant.objects.create(
                restuarant_name = restuarant_name,
                location = location,
                cuisine = cuisine,
                rating = rating,
                picture = picture
                )
            # return HttpResponse("Restuarant added successfully!")
            return render(request,'admin_home.html',{'message':'Restuarant added successfully!'})
def open_show_restuarant(request):
    restuarantsList = Restuarant.objects.all()
    return render(request,'show_restuarant.html',{'restuarantsList':restuarantsList})
def view_menu(request, restuarant_id, username):
    restuarant = Restuarant.objects.get(id=restuarant_id)
    itemList = restuarant.items.all()
    return render(request, 'customer_menu.html', {'itemList': itemList, 'username': username})
def open_update_restuarant(request,restuarant_id):
    return update_restuarant(request, restuarant_id)

def update_restuarant(request, restuarant_id):
    restuarant = Restuarant.objects.get(id=restuarant_id)
    if request.method == 'POST':
        restuarant.restuarant_name = request.POST.get('name') or restuarant.restuarant_name
        restuarant.picture = request.POST.get('picture') or restuarant.picture
        restuarant.cuisine = request.POST.get('cuisine') or restuarant.cuisine
        rating = request.POST.get('rating')
        if rating:
            try:
                restuarant.rating = float(rating)
            except ValueError:
                pass
        restuarant.save()
        return redirect('open_show_restuarant')
    return render(request, 'update_restuarant.html', {'restuarant': restuarant})

def update_menu(request, restuarant_id):
    restuarant = Restuarant.objects.get(id=restuarant_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')
        Items.objects.create(
            restuarant=restuarant,
            name=name,
            description=description,
            price=float(price) if price else 0.0,
            vegeterian=vegeterian,
            picture=picture or ''
        )
        return redirect('update_menu', restuarant_id=restuarant.id)
    itemList = restuarant.items.all()
    return render(request, 'update_menu.html', {'itemList': itemList, 'restaurant': restuarant})

def open_update_menu(request, restuarant_id):
    return redirect('update_menu', restuarant_id=restuarant_id)

def delete_restuarant(request, restuarant_id):
    restuarant = get_object_or_404(Restuarant, id=restuarant_id)
    restuarant.delete()
    return redirect('open_show_restuarant')
def view_menu(request, restuarant_id, username):
    restuarant = Restuarant.objects.get(id = restuarant_id)
    itemList = restuarant.items.all()
    #return HttpResponse("Items collected")
    #itemList = Item.objects.all()
    return render(request, 'customer_menu.html'
                  ,{"itemList" : itemList,
                     "restaurant" : restuarant, 
                     "username":username})
def add_to_cart(request, item_id, username):
    item = Items.objects.get(id = item_id)
    customer = User.objects.get(username = username)

    cart, created = Cart.objects.get_or_create(customer = customer)

    cart.items.add(item)

    return redirect('show_cart', username=username)

def show_cart(request, username):
    customer = User.objects.get(username = username)
    cart = Cart.objects.filter(customer=customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    return render(request, 'cart.html',{"itemList" : items, "total_price" : total_price, "username":username})

def checkout(request, username):
    # Fetch customer and their cart
    customer = get_object_or_404(User, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'checkout.html', {
            'error': 'Your cart is empty!',
        })
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': '1',  # Automatically capture payment
    }
    order = client.order.create(data=order_data)

    # Pass the order details to the frontend
    return render(request, 'checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount': total_price,
    })

def orders(request, username):
    customer = get_object_or_404(User, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    # Fetch cart items and total price before clearing the cart
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    # Clear the cart after fetching its details
    if cart:
        cart.items.clear()

    return render(request, 'orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
    })
    
