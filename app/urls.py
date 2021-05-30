from django.contrib import admin
from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import LoginForm, MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name="home"),
    path('productdetail/<int:pk>', views.ProductDetailView.as_view(), name="productdetail"),
    path('cart', views.cart, name="cart"),
    path('wish', views.wish, name="wish"),
    path('place-order', views.place_order,name="place-order"),
    path('place-order-directly', views.place_order_directly,name="place-order-directly"),
    # path('login', views.login, name="login"),
    path('accounts/login', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('showcart', views.show_cart, name="showcart"),
    path('showwishlist', views.showwishlist, name="showwishlist"),
    path('paymentdone', views.payment_done, name="paymentdone"),
    path('registration', views.CustomerRegsitrationView.as_view(), name="registration"),
    # path('doRegistration', views.doRegistration, name="doRegistration"),
    path('doLogin', views.doLogin, name="doLogin"),
    path('profile', views.ProfileView.as_view(), name="profile"),
    path('address', views.address, name="address"),
    path('orders', views.orders, name="orders"),
    path('changepassword', views.changepassword, name="changepassword"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name ='password_reset_complete'),
    path('mobile', views.mobile, name="mobile"),
    path('mobile/<slug:data>', views.mobile, name="mobiledata"),
    path('laptop', views.laptop, name="laptop"),
    path('laptop/<slug:data>', views.laptop, name="laptopdata"),
    path('foot', views.foot, name="foot"),
    path('paymentdonedirectly', views.payment_done_directly, name="paymentdonedirectly"),
    path('foot/<slug:data>', views.foot, name="footdata"),
    path('top', views.top, name="top"),
    path('corona', views.corona, name="corona"),
    path('corona/<slug:data>', views.corona, name="coronadata"),
    path('countcart', views.count_cart, name="countcart"),
    path('pluscart', views.plus_cart, name="pluscart"),
    path('minuscart', views.minus_cart, name="minuscart"),
    path('top/<slug:data>', views.top, name="topdata"),
    path('bottom', views.bottom, name="bottom"),
    path('removecart', views.remove_cart, name="removecart"),
    path('removewish', views.remove_wish, name="removewish"),
    path('bottom/<slug:data>', views.bottom, name="bottomdata"),
    path('logout', views.logout_user, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
