from django.urls import path,include
from . import views
urlpatterns=[
    path('',views.index,name="index"),
    path('index',views.index,name="index"),
    path('login',views.login, name="login"),
    path('booking',views.booking, name="booking"),
    path('register',views.register,name="register"),
    path('payment',views.payment,name="payment"),
    path('mybookings',views.mybookings,name="mybookings"),
    path('logout', views.logout, name="logout"),
    path('ticketbooking',views.ticketbooking,name="ticketbooking"),
    path('errorpage',views.errorpage, name="errorpage"),
    path('cancelbooking', views.cancelbooking, name="cancelbooking")
]