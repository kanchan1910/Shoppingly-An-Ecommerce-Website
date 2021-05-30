
from django.shortcuts import render, HttpResponseRedirect,redirect
from .models import Customer, Product, Cart, OrderPlaced, Wish
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomerProfileForm
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomerRegistrationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

# def home(request):
# 	return render(request, 'home.html')

class HomeView(View):
	def get(self, request):
		totalitem = 0
		topwears = Product.objects.filter(category="TW")
		bottomwears = Product.objects.filter(category="BW")
		footwears = Product.objects.filter(category="FW")
		mobiles = Product.objects.filter(category="M")
		laptops = Product.objects.filter(category="L")
		deals = Product.objects.filter(category="D")
		corona = Product.objects.filter(category="C")
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		return render(request, 'home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'footwears': footwears, 'mobiles': mobiles, 'laptops': laptops, 'deals': deals, 'corona': corona, 'totalitem' : totalitem})
	
#
# def product_detail(request):
# 	return render(request, 'productdetails.html')

class ProductDetailView(View):
	def get(self, request, pk):
		totalitem = 0
		user = request.user
		product = Product.objects.get(pk=pk)
		item_already_in_cart = False
		item_already_in_wish = False
		if user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
			item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=user)).exists()
			item_already_in_wish = Wish.objects.filter(Q(product=product.id) & Q(user=user)).exists()

		return render(request, 'productdetails.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem, 'item_already_in_wish':item_already_in_wish})


	
# @login_required
def cart(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect('accounts/login')
	user = request.user
	product_id= request.GET.get('prod_id')
	product = Product.objects.get(id=product_id)
	cart = Cart(user=user,product=product)
	cart.save()
	return redirect('showcart')

# @login_required
def show_cart(request):
	totalitem = 0
	if not request.user.is_authenticated:
			return HttpResponseRedirect('accounts/login')
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0.0
		shipping_charges = 50.0
		total = 0.0
		cart_product = [p for p in Cart.objects.all() if p.user==user]
		if cart_product:
			for p in cart_product:
				temp_amount = (p.quantity * p.product.discounted_price)
				amount += temp_amount
			total += amount + shipping_charges
			return render(request, 'addtocart.html', {'carts':cart, 'total_amount':total, 'amount':amount, 'totalitem':totalitem})
		else:
			return render(request, 'empty.html', {'totalitem':totalitem})


def wish(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect('accounts/login')
	user = request.user
	product_id= request.GET.get('prod_id')
	product = Product.objects.get(id=product_id)
	wish = Wish(user=user,product=product)
	wish.save()
	return redirect('showwishlist')


def showwishlist(request):
	totalitem = 0
	if not request.user.is_authenticated:
			return HttpResponseRedirect('accounts/login')
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
		user = request.user
		wish = Wish.objects.filter(user=user)
		wish_product = [p for p in Wish.objects.all() if p.user==user]
		if wish_product:
			return render(request, 'addtowish.html', {'wishes':wish, 'totalitem':totalitem})
		else:
			return render(request, 'emptywish.html', {'totalitem':totalitem})
		
# @login_required
def place_order(request):
	totalitem = 0
	if not request.user.is_authenticated:
			return HttpResponseRedirect('accounts/login')
	user = request.user
	address = Customer.objects.filter(user=user)
	cart_items = Cart.objects.filter(user=user)
	amount = 0.0
	shipping_charges = 50.0
	total = 0.0
	cart_product = [p for p in Cart.objects.all() if p.user==user]
	if cart_product:
		for p in cart_product:
			temp_amount = (p.quantity * p.product.discounted_price)
			amount += temp_amount
		total += amount + shipping_charges
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if not address:
		messages.add_message(request, messages.SUCCESS, 'Kindly add your shipping address details !')
		return render(request, 'emptyaddress.html', {'add':address, 'total':total, 'cart_items':cart_items, 'amount':amount, 'totalitem':totalitem})
	return render(request, 'place-order.html', {'add':address, 'total':total, 'cart_items':cart_items, 'amount':amount, 'totalitem':totalitem})

def place_order_directly(request):
	totalitem = 0
	if not request.user.is_authenticated:
		return HttpResponseRedirect('accounts/login')
	user = request.user
	product_id= request.GET.get('prod_id')
	product = Product.objects.get(id=product_id)
	# print("here")
	# print(product_id)
	
	address = Customer.objects.filter(user=user)
	amount = product.discounted_price
	shipping_charges = 50.0
	total = amount + shipping_charges
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))

	return render(request, 'place-order-directly.html', {'product':product, 'add':address, 'total':total,  'amount':amount, 'totalitem':totalitem})

#
# def login(request):
# 	return render(request, 'login.html')


# @login_required
def payment_done(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect('accounts/login')
	user=request.user
	customerid = request.GET.get('cusid')
	# use get() when you want to get a single unique object, and filter() when you want to get all objects that match your lookup parameters.
	customer = Customer.objects.get(id=customerid)
	cart = Cart.objects.filter(user=user)
	for c in cart:
		OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
		c.delete()
	messages.add_message(request, messages.SUCCESS, ' Payment completed successfully! Your order is now being processed. Please find your order status below. Wiss you a happy experience !!!')
	return redirect("orders")

def payment_done_directly(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect('accounts/login')
	user=request.user
	customerid = request.GET.get('cusid')
	
	# use get() when you want to get a single unique object, and filter() when you want to get all objects that match your lookup parameters.
	customer = Customer.objects.get(id=customerid)
	product_id= request.GET.get('prod_id')
	product = Product.objects.get(id=product_id)
	OrderPlaced(user=user, customer=customer, product=product, quantity=1).save()
	messages.add_message(request, messages.SUCCESS, ' Payment completed successfully! Your order is now being processed. Please find your order status below. Wiss you a happy experience !!!')
	return redirect("orders")

	
	
	
	
# def registration(request):
# 	return render(request, 'registration.html')

# def profile(request):
# 	return render(request, 'profile.html')


class CustomerRegsitrationView(View):
	def get(self, request):
		form = CustomerRegistrationForm
		return render(request, 'registration.html', {'form':form})
	def post(self, request):
		form = CustomerRegistrationForm(request.POST)
		if form.is_valid():
			messages.error(request, 'Congratulations !! Registered Successfully')
			form.save()
		return render(request, 'registration.html', {'form':form})


# @login_required
def address(request):
	totalitem = 0
	if not request.user.is_authenticated:
			return HttpResponseRedirect('accounts/login')
	add = Customer.objects.filter(user=request.user)
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	return render(request, 'address.html', {'add':add, 'active':'btn-primary', 'totalitem': totalitem})

# @login_required
def orders(request):
	totalitem = 0
	if not request.user.is_authenticated:
			return HttpResponseRedirect('accounts/login')
	user = request.user
	op = OrderPlaced.objects.filter(user=user)
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if not op:
		return render(request, 'emptyorder.html', {'totalitem':totalitem})
	return render(request, 'orders.html', {'order_placed':op, 'totalitem':totalitem})

# @login_required
def changepassword(request):
	totalitem = 0
	if not request.user.is_authenticated:
			return HttpResponseRedirect('accounts/login')
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	return render(request, 'changepassword.html', {'totalitem':totalitem})



	

def corona(request, data=None):
	if(data == None):
		coronas = Product.objects.filter(category = "C")
	elif(data == 'Masks' or data == 'Oximeter' or data == 'Gloves' or data == 'PPEKits' or data == 'HandSanitizer'):
		coronas = Product.objects.filter(category = "C").filter(brand=data)
	return render(request, 'corona.html', {'corona':coronas})

def mobile(request, data=None):
	totalitem = 0
	if(data == None):
		mobiles = Product.objects.filter(category = "M")
	elif(data == 'Apple' or data == 'Redmi' or data == 'Oppo' or data == 'Nokia'):
		mobiles = Product.objects.filter(category = "M").filter(brand=data)
	elif(data == "below"):
		mobiles = Product.objects.filter(category = "M").filter(discounted_price__lt = 10000)
	elif(data == "above"):
		mobiles = Product.objects.filter(category = "M").filter(discounted_price__gt = 10000)
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	return render(request, 'mobile.html', {'mobiles':mobiles, 'totalitem':totalitem})
	
def laptop(request, data=None):
	totalitem = 0
	if(data == None):
		laptops = Product.objects.filter(category = "L")
	elif(data == 'Apple' or data == 'Asus' or data == 'Acer' or data == 'hp'):
		laptops = Product.objects.filter(category = "L").filter(brand=data)
	elif(data == "below"):
		laptops = Product.objects.filter(category = "L").filter(discounted_price__lt = 100000)
	elif(data == "above"):
		laptops = Product.objects.filter(category = "L").filter(discounted_price__gt = 100000)
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	return render(request, 'laptop.html', {'laptops':laptops, 'totalitem':totalitem})
	
	
def foot(request, data=None):
	totalitem = 0
	if(data == None):
		foots = Product.objects.filter(category = "FW")
	elif(data == 'Shoes' or data == 'Bellies' or data == 'Sleepers' or data == 'Sandles'):
		foots = Product.objects.filter(category = "FW").filter(brand=data)
	elif(data == "below"):
		foots = Product.objects.filter(category = "FW").filter(discounted_price__lt = 350)
	elif(data == "above"):
		foots = Product.objects.filter(category = "FW").filter(discounted_price__gt = 350)
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	return render(request, 'foot.html', {'foots':foots, 'totalitem':totalitem})
	
	
def top(request, data=None):
	totalitem = 0
	if(data == None):
		tops = Product.objects.filter(category = "TW")
	elif(data == 'Girls' or data == 'Boys'):
		tops = Product.objects.filter(category = "TW").filter(brand=data)
	elif(data == "below"):
		tops = Product.objects.filter(category = "TW").filter(discounted_price__lt = 1000)
	elif(data == "above"):
		tops = Product.objects.filter(category = "TW").filter(discounted_price__gt = 1000)
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	return render(request, 'top.html', {'tops':tops, 'totalitem':totalitem})

def bottom(request, data=None):
	totalitem = 0
	if(data == None):
		bottoms = Product.objects.filter(category = "BW")
	elif(data == 'Girls' or data == 'Boys'):
		bottoms = Product.objects.filter(category = "BW").filter(brand=data)
	elif(data == "below"):
		bottoms = Product.objects.filter(category = "BW").filter(discounted_price__lt = 1000)
	elif(data == "above"):
		bottoms = Product.objects.filter(category = "BW").filter(discounted_price__gt = 1000)
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	return render(request, 'bottom.html', {'bottoms':bottoms, 'totalitem':totalitem})


#
# def doRegistration(request):
# 	print(request.GET)
# 	email_id = request.GET.get('email')
# 	password = request.GET.get('password')
# 	username = request.GET.get('username')
# 	confirm_password = request.GET.get('confirmPassword')
# 	print(email_id)
# 	print(username)
# 	print(password)
# 	print(confirm_password)
# 	if not (email_id and username and password and confirm_password):
# 		messages.error(request, 'Please provide all the details!!')
# 		return render(request, 'registration.html')
#
# 	if password != confirm_password:
# 		messages.error(request, 'Both passwords should match!!')
# 		return render(request, 'registration.html')
#
# 	is_user_exists = User.objects.filter(email=email_id).exists()
#
# 	if is_user_exists:
# 		messages.error(request, 'User with this email id already exists. Please proceed to login!!')
# 		return render(request, 'registration.html')
#
# 	is_username_exists = User.objects.filter(username=username).exists()
#
# 	if is_username_exists:
# 		messages.error(request, 'This username is already taken!!')
# 		return render(request, 'registration.html')
#
#
# 	u1 = User()
# 	u1.email = email_id
# 	u1.username = username
# 	u1.password = password
# 	u1.save()
# 	cus = Customer()
# 	cus.user = u1
# 	cus.save()
# 	return render(request, 'login.html')

def doLogin(request):

	username = request.GET.get('username')
	password = request.GET.get('password')
	print(username)
	print(password)
	print(request.user)
	
	# user = User.objects.filter(email=email_id, password=password).first()
	
	# if not user:
	# 	messages.error(request, 'Invalid Login Credentials!!')
	# 	return render(request, 'login.html')
	#
	# customer = Customer.objects.filter(user=user).first()
	#
	# if not customer:
	# 	messages.error(request, 'User Not registered!!')
	# 	return render(request, 'registration.html')

	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect("profile")
	else:
		messages.error(request, 'Invalid Login Credentials!!')
		return render(request, 'login.html')
	
	return render(request, 'login.html')

def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product = prod_id) & Q(user=request.user ))
		c.quantity += 1
		c.save()
		amount = 0.0
		shipping_amount = 50.0
		total = 0
		cart_product = [p for p in Cart.objects.all() if p.user==request.user]
		for p in cart_product:
			temp_amount = (p.quantity * p.product.discounted_price)
			amount += temp_amount
		total += amount + shipping_amount
		data={
			'quantity': c.quantity,
			'amount': amount,
			'total': total
		}
		return JsonResponse(data)
	
	
def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product = prod_id) & Q(user=request.user ))
		c.quantity -= 1
		c.save()
		amount = 0.0
		shipping_amount = 50.0
		total = 0
		cart_product = [p for p in Cart.objects.all() if p.user==request.user]
		for p in cart_product:
			temp_amount = (p.quantity * p.product.discounted_price)
			amount += temp_amount
		total += amount + shipping_amount
		data={
			'quantity': c.quantity,
			'amount': amount,
			'total': total
		}
		return JsonResponse(data)


def count_cart(request):
	total_items_in_cart = 0
	if request.user.is_authenticated:
		total_items_in_cart = len(Cart.objects.filter(user=request.user))
	data={
		'total_items_in_cart':total_items_in_cart
	}
	return JsonResponse(data)

	
def remove_cart(request):
	total_items_in_cart = 0
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product = prod_id) & Q(user=request.user ))
		c.delete()
		amount = 0.0
		shipping_amount = 50.0
		total = 0
		cart_product = [p for p in Cart.objects.all() if p.user==request.user]
		for p in cart_product:
			temp_amount = (p.quantity * p.product.discounted_price)
			amount += temp_amount
		total += amount + shipping_amount
		if request.user.is_authenticated:
			total_items_in_cart = len(Cart.objects.filter(user=request.user))
			
		data={
			'amount': amount,
			'total': total,
			'total_items_in_cart':total_items_in_cart
		}
		return JsonResponse(data)

def remove_wish(request):
	total_items_in_cart = 0
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		w = Wish.objects.get(Q(product = prod_id) & Q(user=request.user ))
		w.delete()
		if request.user.is_authenticated:
			total_items_in_cart = len(Cart.objects.filter(user=request.user))
			
		data={
			'total_items_in_cart':total_items_in_cart
		}
		return JsonResponse(data)
	

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

# @method_decorator(login_required,name='dispatch')
class ProfileView(View):
	def get(self, request):
		totalitem=0
		# To prevent anonymous user to access profile , we will send them to the login page
		# this is the another method of doing the same thing by avoiding decorators
		if not request.user.is_authenticated:
			return HttpResponseRedirect('login')
		form = CustomerProfileForm()
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		return render(request, 'profile.html', {'form':form, 'active' : 'btn-primary', 'totalitem':totalitem})
	def post(self, request):
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user= usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated successfully! You can verify your shipping address details...')
			# form.save()
			return render(request, 'profile.html', {'form':form, 'active':'btn-primary'})
