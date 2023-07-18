from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm,PasswordResetForm,ChangePasswordForm,SetPasswordForm

urlpatterns = [
    path("", views.home),
    path('about/', views.about,name="about"),
    path('contact/', views.contact,name="contact"),
    path("category/<slug:val>", views.CategoryView.as_view(),name="category"),
    path("category-title/<val>", views.CategoryTitle.as_view(),name="category-title"),
    path("products-detail/<int:pk>", views.ProductsDetail.as_view(),name="products-detail"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateaddress/<int:pk>', views.UpdateAddress.as_view(), name='updateaddress'),
    
    path('add-to-cart/',views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/',views.checkout.as_view(),name='checkout'),
    path('paymentdone/',views.payment_done,name="paymentdone"),
    path('orders/',views.orders, name='orders'),
    
    path('search/',views.search,name='search'),
    path('wishlist/',views.show_wishlist,name='wishlist'),
    
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('pluswishlist/',views.plus_wishlist),
    path('minuswishlist/',views.minus_wishlist),
    
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', auth_view.LoginView.as_view(template_name='cart/login.html', authentication_form=LoginForm), name='login'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='cart/password_reset.html', form_class=PasswordResetForm), name='password_reset'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='cart/changepassword.html',form_class=ChangePasswordForm, success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='cart/passwordchangedone.html'),name='passwordchangedone'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='cart/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='cart/password_reset_confirm.html',form_class=SetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='cart/password_reset_complete.html'),name='password_reset_complete'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Men's Apparel"
admin.site.site_title = "Men's Apparel"
admin.site.site_index_title = "Welcome to Men's Apparel"