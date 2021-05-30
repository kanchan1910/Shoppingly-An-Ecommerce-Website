from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
	 ("Andhra Pradesh", "Andhra Pradesh"),
     ("Arunachal Pradesh", "Arunachal Pradesh"),
	 ("Assam", "Assam"),
	 ("Bihar", "Bihar"),
	 ("Chhattisgarh", "Chhattisgarh"),
	 ("Goa", "Goa"),
     ("Gujarat", "Gujarat"),
	 ("Haryana", "Haryana"),
	 ("Himachal Pradesh", "Himachal Pradesh"),
	 ("Jharkhand", "Jharkhand"),
	 ("Karnataka", "Karnataka"),
     ("Kerala", "Kerala"),
	 ("Madhya Pradesh", "Madhya Pradesh"),
	 ("Maharashtra", "Maharashtra"),
	 ("Manipur", "Manipur"),
	 ("Meghalaya", "Meghalaya"),
	 ("Mizoram", "Mizoram"),
     ("Odisha", "Odisha"),
	 ("Punjab", "Punjab"),
	 ("Rajasthan", "Rajasthan"),
	 ("Tamil Nadu", "Tamil Nadu"),
	 ("Telangana", "Telangana"),
	 ("Uttar Pradesh", "Uttar Pradesh"),
	 ("Uttarakhand", "Uttarakhand"),
	 ("West Bengal", "West Bengal"),
)

class Customer(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	locality = models.CharField(max_length=200)
	city = models.CharField(max_length=50)
	zipcode = models.IntegerField(null=True)
	state = models.CharField(choices=STATE_CHOICES, max_length=100)
	
	def __str__(self):
		return str(self.id)
	
CATEGORY_CHOICES = (
	('M', 'Mobile'),
	('L', 'Laptop'),
	('TW', 'Top Wear'),
	('BW', 'Bottom Wear'),
	('FW', 'Foot Wear'),
	('D', 'Deal'),
	('C', 'Corona'),
)

class Product(models.Model):
	title = models.CharField(max_length=200)
	selling_price = models.FloatField()
	discounted_price = models.FloatField()
	description = models.TextField()
	brand = models.CharField(max_length=100)
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
	product_image = models.FileField(upload_to='product_img')
	
	def __str__(self):
		return str(self.id)
	
class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	
	def __str__(self):
		return str(self.id)
	
	
class Wish(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	
	def __str__(self):
		return str(self.id)


STATUS_CHOICES = (
	('Accepted', 'Accepted'),
	('Packed', 'Packed'),
	('On The Way', 'On The Way'),
	('Delivered', 'Delivered'),
	('Cancel', 'Cancel'),
)

class OrderPlaced(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	order_date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
	



# Create your models here.
